import logging
import time
from uuid import UUID

from bx_django_utils.models.manipulate import CreateOrUpdateResult
from django.contrib import admin, messages
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from fritzconnection.core.exceptions import FritzLookUpError
from reversion_compare.admin import CompareVersionAdmin

from djfritz.models.hosts import HostModel
from djfritz.services.hosts import (
    collect_host_info,
    set_wan_access_with_messages,
    update_host,
    update_hosts,
)


logger = logging.getLogger(__name__)


class NameUniquenessFilter(admin.SimpleListFilter):
    title = _('unique name')
    parameter_name = 'uniqueness'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value():
            data = (
                queryset.values('name')
                .order_by('name')
                .annotate(name_count=Count('name'))
                .filter(name_count=1)
            )
            unique_names = {entry['name'] for entry in data}

        if self.value() == 'yes':
            return queryset.filter(name__in=unique_names)

        if self.value() == 'no':
            return queryset.exclude(name__in=unique_names)


@admin.register(HostModel)
class HostModelAdmin(CompareVersionAdmin):
    change_list_template = 'admin/djfritz/hostmodel/change_list.html'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('tags')
        return qs

    @admin.display(ordering='name', description=_('HostModel.name.verbose_name'))
    def verbose_name(self, obj):
        return render_to_string(
            template_name='admin/djfritz/hostmodel/column_verbose_name.html',
            context={'obj': obj},
        )

    def host_name_info_view(self, request):
        start_time = time.monotonic()
        pks = request.GET.getlist('pk')
        assert pks
        queryset = HostModel.objects.filter(pk__in=pks)
        names = sorted(queryset.order_by('name').values_list('name', flat=True).distinct())
        assert names

        data = collect_host_info(names=names)
        context = {
            'data': data,
            'title': _('Host name info'),
            'opts': self.opts,
            **self.admin_site.each_context(request),
        }
        duration = time.monotonic() - start_time
        messages.info(request, f'Information collected in {duration:.1f} sec')
        return TemplateResponse(request, 'djfritz/host_name_info.html', context)

    @admin.action(description='Get host name info')
    def host_name_info(self, request, queryset):
        pks = '&'.join(f'pk={pk}' for pk in queryset.values_list('pk', flat=True))

        opts = self.model._meta
        url = reverse(
            f'admin:{opts.app_label}_{opts.model_name}_host_name_info',
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(f'{url}?{pks}')

    search_fields = ('name', 'tags__name')
    list_display = (
        'verbose_name',
        'wan_access',
        'last_status',
        'update_dt',
        'ip_v4',
        'mac',
        'create_dt',
    )
    list_display_links = ('verbose_name',)
    list_filter = (
        'last_status',
        'wan_access',
        'interface_type',
        'address_source',
        'group',
        'tags',
        NameUniquenessFilter,
    )
    date_hierarchy = 'create_dt'
    readonly_fields = ('wan_access',)
    ordering = ('-last_status', '-update_dt')
    actions = (host_name_info,)

    def get_urls(self):
        urls = super().get_urls()
        opts = self.model._meta
        urls += [
            path(
                route='update_hosts',
                view=self.admin_site.admin_view(self.update_hosts_view, cacheable=False),
                name=f'{opts.app_label}_{opts.model_name}_update_hosts',
            ),
            path(
                route='update_host/<uuid:object_id>',
                view=self.admin_site.admin_view(self.update_host_view, cacheable=False),
                name=f'{opts.app_label}_{opts.model_name}_update_host',
            ),
            path(
                route='allow_wan_access/<uuid:object_id>',
                view=self.admin_site.admin_view(self.allow_wan_access_view, cacheable=False),
                name=f'{opts.app_label}_{opts.model_name}_allow_wan_access',
            ),
            path(
                route='disallow_wan_access/<uuid:object_id>',
                view=self.admin_site.admin_view(self.disallow_wan_access_view, cacheable=False),
                name=f'{opts.app_label}_{opts.model_name}_disallow_wan_access',
            ),
            path(
                route='host_name_info',
                view=self.admin_site.admin_view(self.host_name_info_view, cacheable=False),
                name=f'{opts.app_label}_{opts.model_name}_host_name_info',
            ),
        ]
        return urls

    def get_object_or_404(self, object_id):
        assert isinstance(object_id, UUID)
        obj = get_object_or_404(self.model, pk=object_id)
        return obj

    def redirect2change(self, obj):
        url = obj.get_change_url()
        return HttpResponseRedirect(url)

    def update_hosts_view(self, request, extra_context=None):
        msg = update_hosts()
        messages.info(request, msg)

        opts = self.model._meta
        url = reverse(
            f'admin:{opts.app_label}_{opts.model_name}_changelist',
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

    def update_host_view(self, request, object_id, extra_context=None):
        obj = self.get_object_or_404(object_id)
        try:
            result: CreateOrUpdateResult = update_host(host=obj)
        except FritzLookUpError as err:
            messages.error(request, f'Error updating {obj}: {err}')
        else:
            if result.updated_fields:
                messages.success(request, f'Updated: {", ".join(result.updated_fields)}')
            else:
                messages.info(request, 'No changed, all values up-to-date')
        return self.redirect2change(obj)

    def set_wan_access_state(self, request, object_id, allow: bool):
        host: HostModel = self.get_object_or_404(object_id)
        set_wan_access_with_messages(request=request, host=host, allow=allow)
        return self.redirect2change(host)

    def allow_wan_access_view(self, request, object_id, extra_context=None):
        logger.info('Allow WAN access to %r', object_id)
        return self.set_wan_access_state(request, object_id, allow=True)

    def disallow_wan_access_view(self, request, object_id, extra_context=None):
        logger.info('Disallow WAN access to %r', object_id)
        return self.set_wan_access_state(request, object_id, allow=False)

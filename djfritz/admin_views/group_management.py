from bx_django_utils.admin_extra_views.base_view import AdminExtraViewMixin
from bx_django_utils.admin_extra_views.datatypes import AdminExtraMeta
from bx_django_utils.admin_extra_views.registry import register_admin_view
from django.contrib import messages
from django.contrib.admin.utils import unquote
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from djfritz.admin_views.base_views import DjangoAdminContextMixin, management_app
from djfritz.models import HostGroupModel
from djfritz.services.hosts import set_wan_access_with_messages


@register_admin_view(pseudo_app=management_app)
class GroupManagementView(AdminExtraViewMixin, DjangoAdminContextMixin, TemplateView):
    meta = AdminExtraMeta(name='Manage host WAN access via host-groups')

    title = 'Manage host WAN access via host-groups'
    template_name = 'djfritz/group_management.html'

    def get(self, request, *args, **kwargs):
        group_pk = request.GET.get('group')
        wan_access = request.GET.get('wan_access')
        if group_pk and wan_access:
            assert wan_access in ('allow', 'disallow')
            group_pk = unquote(group_pk)
            host_group = get_object_or_404(HostGroupModel, pk=group_pk)
            hosts_qs = host_group.hosts.all()
            for host in hosts_qs:
                if not host.ip_v4:
                    messages.info(request, f'Skip {host} because IP address not set')
                else:
                    set_wan_access_with_messages(
                        request=request, host=host, allow=wan_access == 'allow'
                    )

            return HttpResponseRedirect(request.path)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **context):
        groups_qs = HostGroupModel.objects.all()
        groups_qs = groups_qs.prefetch_related('hosts')
        groups_qs = groups_qs.annotate(num_hosts=Count('hosts'))
        context['groups'] = groups_qs
        return super().get_context_data(**context)

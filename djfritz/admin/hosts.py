from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from reversion_compare.admin import CompareVersionAdmin

from djfritz.models.hosts import HostModel
from djfritz.services.hosts import update_hosts


@admin.register(HostModel)
class HostModelAdmin(CompareVersionAdmin):
    change_list_template = 'admin/djfritz/hostmodel/change_list.html'

    search_fields = ('name', 'tags__name')
    list_display = ('mac', 'name', 'last_status', 'update_dt', 'interface_type')
    list_display_links = ('name',)
    list_filter = ('last_status', 'interface_type', 'address_source', 'tags')
    date_hierarchy = 'create_dt'

    def get_urls(self):
        urls = super().get_urls()
        opts = self.model._meta
        urls.append(
            path(
                route='update',
                view=self.admin_site.admin_view(self.update_hosts_view),
                name=f"{opts.app_label}_{opts.model_name}_update_hosts",
            )
        )
        return urls

    def update_hosts_view(self, request, extra_context=None):
        msg = update_hosts()
        messages.info(request, msg)

        opts = self.model._meta
        url = reverse(
            f"admin:{opts.app_label}_{opts.model_name}_changelist",
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

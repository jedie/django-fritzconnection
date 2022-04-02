from bx_django_utils.humanize.pformat import pformat
from django.views.generic import TemplateView
from fritzconnection.lib.fritzhosts import FritzHosts

from djfritz.fritz_connection import FritzHostFilter, get_fritz_connection
from djfritz.views.base_views import DjangoAdminContextMixin, OnlyStaffUserMixin


class HostInformationView(OnlyStaffUserMixin, DjangoAdminContextMixin, TemplateView):
    title = 'Get information about registered hosts'
    template_name = 'djfritz/host_information.html'

    def get_context_data(self, **context):
        fc = get_fritz_connection()

        fh = FritzHosts(fc=fc)
        context['hosts'] = sorted(fh.get_hosts_info(), key=lambda x: (not x['status'], x['ip']))
        ip = self.request.GET.get('ip')
        if ip:
            context['current_ip'] = ip

            fhf = FritzHostFilter(fc=fc)

            wan_access = self.request.GET.get('wan_access')
            if wan_access:
                # Change Internet access for one IP address
                if wan_access == 'disallow':
                    disallow_wan_access = 1
                elif wan_access == 'allow':
                    disallow_wan_access = 0
                else:
                    raise TypeError('Unknown value')

                fhf.disallow_wan_access(ip=ip, state=disallow_wan_access)

            context['wan_access_state'] = fhf.wan_access_state(ip=ip)

        return super().get_context_data(**context)


class MeshTopologyView(OnlyStaffUserMixin, DjangoAdminContextMixin, TemplateView):
    title = 'Get raw mesh topology'
    template_name = 'djfritz/mesh_topology.html'

    def get_context_data(self, **context):
        fc = get_fritz_connection()

        fh = FritzHosts(fc=fc)
        mesh_topology = fh.get_mesh_topology()

        context['mesh_topology_pformat'] = pformat(mesh_topology)

        return super().get_context_data(**context)

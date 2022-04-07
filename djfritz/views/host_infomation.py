import datetime
import sys

from bx_django_utils.humanize.pformat import pformat
from django.views.generic import TemplateView
from fritzconnection.lib.fritzhosts import FritzHosts

from djfritz.fritz_connection import FritzHostFilter, get_fritz_connection
from djfritz.models import HostModel
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


class LastConnectInfoView(OnlyStaffUserMixin, DjangoAdminContextMixin, TemplateView):
    title = 'List "last connect" information about hosts'
    template_name = 'djfritz/last_connect_info.html'

    def get_context_data(self, **context):
        fc = get_fritz_connection()
        fh = FritzHosts(fc=fc)
        mesh_topology = fh.get_mesh_topology()
        nodes = mesh_topology['nodes']

        master_oldest_timestamp = sys.maxsize
        mac_last_connected = {}
        for node in nodes:
            is_master = node['mesh_role'] == 'master'

            node_interfaces = node['node_interfaces']
            for node_interface in node_interfaces:
                mac_address = node_interface['mac_address']
                last_known_connected = mac_last_connected.get(mac_address, 0)
                node_links = node_interface['node_links']
                for node_link in node_links:
                    last_connected = node_link['last_connected']
                    if last_connected > last_known_connected:
                        mac_last_connected[mac_address] = last_connected

                    if is_master and last_connected < master_oldest_timestamp:
                        master_oldest_timestamp = last_connected

        data = []
        for mac_address, last_connected in mac_last_connected.items():
            host = HostModel.objects.filter(mac=mac_address).first()

            # "last_connect" is a UNIX timestamp
            last_connected_dt = datetime.datetime.fromtimestamp(
                last_connected, tz=datetime.timezone.utc
            )
            data.append(
                {
                    'host': host,
                    'mac_address': mac_address,
                    'last_connected': last_connected,
                    'last_connected_dt': last_connected_dt,
                    'faulty_timestamp': last_connected == master_oldest_timestamp,
                }
            )

        context['data'] = data
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

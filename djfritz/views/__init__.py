from bx_django_utils.view_utils.dynamic_menu_urls import DynamicViewMenu

from djfritz.views.diagnose import FritzBoxConnectionView, ListBoxServicesView
from djfritz.views.group_management import GroupManagementView
from djfritz.views.host_infomation import HostInformationView, LastConnectInfoView, MeshTopologyView


dynamic_view_menu = DynamicViewMenu()


dynamic_view_menu.add_views(
    app_name='djfritz',
    menu=(
        (
            'Management',
            {
                'views': ((GroupManagementView, 'group_management'),),
            },
        ),
        (
            'Host information',
            {
                'views': (
                    (HostInformationView, 'host_information'),
                    (LastConnectInfoView, 'last_connect_info'),
                    (MeshTopologyView, 'mesh_information'),
                ),
            },
        ),
        (
            'Diagnose',
            {
                'views': (
                    (FritzBoxConnectionView, 'diagnose_connection'),
                    (ListBoxServicesView, 'list_box_services'),
                ),
            },
        ),
    ),
)

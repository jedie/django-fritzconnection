from bx_django_utils.view_utils.dynamic_menu_urls import DynamicViewMenu

from djfritz.views.diagnose import FritzBoxConnectionView, HostInformationView, ListBoxServicesView


dynamic_view_menu = DynamicViewMenu()


dynamic_view_menu.add_views(
    app_name='djfritz',
    menu=(
        (
            'Diagnose',
            {
                'views': (
                    (FritzBoxConnectionView, 'diagnose_connection'),
                    (HostInformationView, 'host_information'),
                    (ListBoxServicesView, 'list_box_services'),
                )
            },
        ),
    ),
)

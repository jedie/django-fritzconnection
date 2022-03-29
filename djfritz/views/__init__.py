from bx_django_utils.view_utils.dynamic_menu_urls import DynamicViewMenu

from djfritz.views.diagnose import FritzBoxConnectionView


dynamic_view_menu = DynamicViewMenu()


dynamic_view_menu.add_views(
    app_name='djfritz',
    menu=(
        (
            'Diagnose',
            {'views': ((FritzBoxConnectionView, 'diagnose_connection'),)},
        ),
    ),
)

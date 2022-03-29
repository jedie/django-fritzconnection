from django.views.generic import TemplateView
from fritzconnection import __version__ as fc_version

from djfritz.fritz_connection import get_fritz_connection
from djfritz.views.base_views import OnlyStaffUserMixin


class FritzBoxConnectionView(OnlyStaffUserMixin, TemplateView):
    title = 'Test FritzBox connection'
    template_name = 'djfritz/diagnose_connection.html'

    def get_context_data(self, **context):
        fc = get_fritz_connection()

        system_info = fc.device_manager.system_info
        if system_info:
            context.update(
                dict(
                    system=system_info[-1],
                    build=system_info[-2],
                    hw_code=system_info[0],
                )
            )

        context.update(
            dict(
                fritzconnection_version=fc_version,
                last_connection=get_fritz_connection.last_connection,
                modelname=fc.modelname,
                address=fc.soaper.address,
                system_version=fc.system_version
            )
        )
        return super().get_context_data(**context)

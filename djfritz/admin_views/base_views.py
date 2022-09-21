from bx_django_utils.admin_extra_views.datatypes import AdminExtraMeta, PseudoApp
from django.contrib.admin import site


management_app = PseudoApp(meta=AdminExtraMeta(name='Management'))
host_info_app = PseudoApp(meta=AdminExtraMeta(name='Host information'))
diagnose_app = PseudoApp(meta=AdminExtraMeta(name='Diagnose'))


class DjangoAdminContextMixin:
    def get_context_data(self, **context):
        extra = site.each_context(self.request)
        context.update(**extra)
        return super().get_context_data(**context)

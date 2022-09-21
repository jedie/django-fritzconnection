from bx_django_utils.admin_extra_views.base_view import AdminExtraViewMixin
from bx_django_utils.admin_extra_views.datatypes import AdminExtraMeta
from bx_django_utils.admin_extra_views.registry import register_admin_view
from bx_py_utils.anonymize import anonymize
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from fritzconnection import __version__ as fc_version
from fritzconnection.core.fritzconnection import FRITZ_USERNAME

from djfritz.admin_views.base_views import DjangoAdminContextMixin, diagnose_app
from djfritz.fritz_connection import get_fritz_connection


@register_admin_view(pseudo_app=diagnose_app)
class FritzBoxConnectionView(AdminExtraViewMixin, DjangoAdminContextMixin, TemplateView):
    meta = AdminExtraMeta(name='Test FritzBox connection')
    template_name = 'djfritz/diagnose_connection.html'

    def get_context_data(self, **context):
        fc = get_fritz_connection()
        if not fc:
            messages.error(self.request, 'No Connection to FritzBox!')
            return context

        fritz_username = fc.soaper.user
        if fritz_username == FRITZ_USERNAME:
            context['username_info'] = _('(Warning: Default username! Please set a own one!)')

        fritz_password = anonymize(fc.soaper.password)
        if fritz_password:
            context['fritz_password'] = fritz_password
        else:
            context['password_info'] = _('(Please set the FritzBox password!)')

        context.update(
            dict(
                fritz_username=fc.soaper.user,
                fritz_password=anonymize(fc.soaper.password),
            )
        )

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
                system_version=fc.system_version,
            )
        )
        return super().get_context_data(**context)


@register_admin_view(pseudo_app=diagnose_app)
class ListBoxServicesView(AdminExtraViewMixin, DjangoAdminContextMixin, TemplateView):
    meta = AdminExtraMeta(name='List all FritzBox services')
    template_name = 'djfritz/list_box_services.html'

    def get_context_data(self, **context):
        fc = get_fritz_connection()
        if not fc:
            messages.error(self.request, 'No Connection to FritzBox!')
            return context

        context['services'] = fc.services

        service_name = self.request.GET.get('service_name')
        if service_name:
            try:
                service = fc.services[service_name]
            except KeyError:
                messages.error(self.request, 'Invalid service name')
            else:
                context['current_service_name'] = service_name
                actions = service.actions
                context['service_actions'] = actions.keys()
                action_name = self.request.GET.get('action_name')
                if action_name:
                    try:
                        action = service.actions[action_name]
                    except KeyError:
                        messages.error(self.request, 'Invalid service action name')
                    else:
                        context['current_action_name'] = action_name
                        arguments = []
                        for argument in action.arguments.values():
                            var = service.state_variables.get(argument.relatedStateVariable, '')
                            arguments.append(
                                {
                                    'argument_name': argument.name,
                                    'direction': argument.direction,
                                    'data_type': var.dataType,
                                }
                            )

                        context['action_arguments'] = arguments

        return super().get_context_data(**context)

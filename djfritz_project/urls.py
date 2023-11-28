from bx_django_utils.admin_extra_views.registry import extra_view_registry
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.urls import include, path, reverse
from django.views.generic import RedirectView

from djfritz.admin_views.group_management import GroupManagementView


admin.autodiscover()


class Redirect2GroupManagement(RedirectView):
    def get(self, request, *args, **kwargs):
        url = reverse(GroupManagementView.meta.url_name)
        if not request.user.is_authenticated:
            return redirect_to_login(next=url, login_url='admin:login')

        return HttpResponseRedirect(url)


urlpatterns = [  # Don't use i18n_patterns() here
    path('', Redirect2GroupManagement.as_view()),
    path('admin/', include(extra_view_registry.get_urls())),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

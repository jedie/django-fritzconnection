from django.conf import settings
from django.conf.urls import include, static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = [  # Don't use i18n_patterns() here
    path('', RedirectView.as_view(pattern_name='admin:index')),
    path('admin/', admin.site.urls),
    path('', include('djfritz.urls')),
]


if settings.SERVE_FILES:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

from djfritz.views import dynamic_view_menu


app_name = 'djfritz'


urlpatterns = dynamic_view_menu.get_urls()  # Add all views

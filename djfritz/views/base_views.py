from django.contrib.admin import site
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


class DjangoAdminContextMixin:
    def get_context_data(self, **context):
        extra = site.each_context(self.request)
        context.update(**extra)
        return super().get_context_data(**context)


class OnlyStaffUserMixin:
    title = None

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **context):
        assert self.title is not None
        context['title'] = self.title
        return super().get_context_data(**context)

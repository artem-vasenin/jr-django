from django.shortcuts import redirect
from django.views import View


class AnonymousRequiredMixin(View):
    """ Проверка на то, что юзер не авторизован """
    redirect_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class AuthenticatedRequiredMixin(View):
    """ Проверка на то, что юзер авторизован """
    redirect_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class SuperuserRequiredMixin(View):
    """ Проверка на суперадмина """
    redirect_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

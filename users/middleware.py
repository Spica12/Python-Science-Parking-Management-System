from django.shortcuts import reverse, redirect
from .decorators import is_active
from .views import logout

class CheckUserIsActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = [reverse('users:login'), reverse('users:register')]

        if request.user.is_authenticated:
            if not is_active(request.user):
                if request.path not in allowed_urls:
                    logout(request)
                    return redirect('users:login')
        return self.get_response(request)
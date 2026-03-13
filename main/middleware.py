from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    Require authentication for the whole site, except explicit public paths.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)

        path = request.path or "/"

        public_prefixes = (
            settings.LOGIN_URL,
            "/logout/",
            "/admin/",
            "/offline/",
            "/sw.js",
            settings.STATIC_URL,
            settings.MEDIA_URL,
        )

        if any(path.startswith(prefix) for prefix in public_prefixes):
            return self.get_response(request)

        return redirect(f"{settings.LOGIN_URL}?next={path}")

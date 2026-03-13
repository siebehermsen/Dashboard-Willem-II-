from django.conf import settings


def app_flags(request):
    return {
        "APP_UI_ONLY_MODE": getattr(settings, "APP_UI_ONLY_MODE", False),
    }

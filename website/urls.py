from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from main import views  
from django.conf import settings
from django.conf.urls.static import static
from main.views import skinfold_view, huidplooimeting_pdf



urlpatterns = [
    path("sw.js", views.service_worker, name="service_worker"),
    path("offline/", views.offline_page, name="offline_page"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=False,
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),

    # ---------- BASIS ----------
    path("admin/", admin.site.urls),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", RedirectView.as_view(pattern_name="login", permanent=False), name="home"),

    path("add_rehab/", views.add_rehab, name="add_rehab"),
    path("add-birthday/", views.add_birthday, name="add_birthday"),
    path("delete-birthday/<int:pk>/", views.delete_birthday, name="delete_birthday"),
    path("add-youth-guest/", views.add_youth_guest, name="add_youth_guest"),
    path("delete-youth-guest/<int:pk>/", views.delete_youth_guest, name="delete_youth_guest"),

    # ---------- WEEKPROGRAMMA ----------
    path("add-weekday/", views.add_weekday, name="add_weekday"),
    path("edit-weekday/<int:pk>/", views.edit_weekday, name="edit_weekday"),
    path("delete-weekday/<int:pk>/", views.delete_weekday, name="delete_weekday"),

    # ---------- REVALIDATIE ----------
    path("revalidatie/", views.revalidatie, name="revalidatie"),
    path("revalidatie-gym/", views.revalidatie_gym, name="revalidatie_gym"),

    # ---------- PAGINA’S ----------
    path("nutrition/", views.nutrition_view, name="nutrition"),
    path("nutrition/huidplooien/", views.skinfold_view, name="skinfolds"),
    path("training/", views.training, name="training"),
    path("huidplooimeting/", views.skinfold_view, name="huidplooimeting"),
    path("wedstrijd/", views.wedstrijddata, name="wedstrijddata"),
    path("upload_wedstrijddata/", views.upload_wedstrijddata, name="upload_wedstrijddata"),
    path("testdata/", views.testdata, name="testdata"),
    path("wellness/", views.wellness, name="wellness"),
    path("individuele_programmas/", views.individuele_programmas, name="individuele_programmas"),
    path("individueel_programma_opslaan/<int:player_id>/", views.individueel_programma_opslaan, name="individueel_programma_opslaan"),
    path("rpe/", views.rpe_view, name="rpe"),
    path('hit/', views.hit_page, name='hit'),
    path("aanwezigheden/", views.aanwezigheden_pagina, name="aanwezigheden"),
    path("aanwezigheden/update/<int:record_id>/", views.aanwezigheden_update, name="aanwezigheden_update"),
    path("overig/", views.overig, name="overig"),
    path("beweeganalyse/", views.beweeganalyse, name="beweeganalyse"),
    path("huidplooimeting/pdf/", huidplooimeting_pdf, name="huidplooimeting_pdf"),


    # ---------- DATA ----------
    path("seed_data/", views.seed_data, name="seed_data"),
    path("player/<int:player_id>/data/", views.player_data, name="player_data"),
    path("player/<int:player_id>/weights/", views.weight_data, name="weight_data"),

    # ---------- UPLOAD ----------
    path("upload/", views.upload_file, name="upload_file"),
]

# ---------- MEDIA BESTANDEN ----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

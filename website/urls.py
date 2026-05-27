from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from main import views  
from django.conf import settings
from django.conf.urls.static import static
from main.views import skinfold_view, huidplooimeting_pdf
from main.permissions import ROLE_ADMIN, ROLE_MEDICAL, ROLE_PERFORMANCE, ROLE_PLAYER, ROLE_TRAINER, role_required



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
    path("dashboard/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_MEDICAL, ROLE_TRAINER, ROLE_PLAYER, allow_read_only_get=True)(views.dashboard), name="dashboard"),
    path("", RedirectView.as_view(pattern_name="login", permanent=False), name="home"),

    path("add_rehab/", role_required(ROLE_ADMIN, ROLE_MEDICAL)(views.add_rehab), name="add_rehab"),
    path("add-birthday/", role_required(ROLE_ADMIN, ROLE_TRAINER)(views.add_birthday), name="add_birthday"),
    path("delete-birthday/<int:pk>/", role_required(ROLE_ADMIN, ROLE_TRAINER)(views.delete_birthday), name="delete_birthday"),
    path("add-youth-guest/", role_required(ROLE_ADMIN, ROLE_TRAINER)(views.add_youth_guest), name="add_youth_guest"),
    path("delete-youth-guest/<int:pk>/", role_required(ROLE_ADMIN, ROLE_TRAINER)(views.delete_youth_guest), name="delete_youth_guest"),

    # ---------- WEEKPROGRAMMA ----------
    path("add-weekday/", role_required(ROLE_ADMIN, ROLE_TRAINER)(views.add_weekday), name="add_weekday"),
    path("edit-weekday/<int:pk>/", role_required(ROLE_ADMIN, ROLE_TRAINER)(views.edit_weekday), name="edit_weekday"),
    path("delete-weekday/<int:pk>/", role_required(ROLE_ADMIN, ROLE_TRAINER)(views.delete_weekday), name="delete_weekday"),

    # ---------- REVALIDATIE ----------
    path("revalidatie/", role_required(ROLE_ADMIN, ROLE_MEDICAL, allow_read_only_get=True)(views.revalidatie), name="revalidatie"),
    path("revalidatie-gym/", role_required(ROLE_ADMIN, ROLE_MEDICAL, allow_read_only_get=True)(views.revalidatie_gym), name="revalidatie_gym"),

    # ---------- PAGINA’S ----------
    path("nutrition/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_MEDICAL, allow_read_only_get=True)(views.nutrition_view), name="nutrition"),
    path("nutrition/huidplooien/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_MEDICAL, allow_read_only_get=True)(views.skinfold_view), name="skinfolds"),
    path("training/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER, allow_read_only_get=True)(views.training), name="training"),
    path("huidplooimeting/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_MEDICAL, allow_read_only_get=True)(views.skinfold_view), name="huidplooimeting"),
    path("wedstrijd/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER, allow_read_only_get=True)(views.wedstrijddata), name="wedstrijddata"),
    path("fysiek-rapport/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER, allow_read_only_get=True)(views.fysiek_rapport), name="fysiek_rapport"),
    path("upload_wedstrijddata/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE)(views.upload_wedstrijddata), name="upload_wedstrijddata"),
    path("testdata/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, allow_read_only_get=True)(views.testdata), name="testdata"),
    path("wellness/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_MEDICAL, ROLE_TRAINER, ROLE_PLAYER, allow_read_only_get=True)(views.wellness), name="wellness"),
    path("academie/<str:team_code>/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER, allow_read_only_get=True)(views.academie_team), name="academie_team"),
    path("academie/<str:team_code>/speler/<int:player_id>/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER, allow_read_only_get=True)(views.academie_player), name="academie_player"),
    path("individuele_programmas/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER, allow_read_only_get=True)(views.individuele_programmas), name="individuele_programmas"),
    path("individueel_programma_opslaan/<int:player_id>/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER)(views.individueel_programma_opslaan), name="individueel_programma_opslaan"),
    path("rpe/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER, allow_read_only_get=True)(views.rpe_view), name="rpe"),
    path('hit/', role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER, allow_read_only_get=True)(views.hit_page), name='hit'),
    path("aanwezigheden/", role_required(ROLE_ADMIN, ROLE_TRAINER, allow_read_only_get=True)(views.aanwezigheden_pagina), name="aanwezigheden"),
    path("aanwezigheden/update/<int:record_id>/", role_required(ROLE_ADMIN, ROLE_TRAINER)(views.aanwezigheden_update), name="aanwezigheden_update"),
    path("beweeganalyse/", role_required(ROLE_ADMIN, ROLE_MEDICAL, ROLE_PERFORMANCE, allow_read_only_get=True)(views.beweeganalyse), name="beweeganalyse"),
    path("potentials/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_TRAINER, allow_read_only_get=True)(views.potentials), name="potentials"),
    path("beleid/", role_required(ROLE_ADMIN, ROLE_TRAINER, allow_read_only_get=True)(views.beleid), name="beleid"),
    path("overig/", role_required(ROLE_ADMIN, ROLE_TRAINER, allow_read_only_get=True)(views.overig), name="overig"),
    path("staf/", views.staf, name="staf"),
    path("huidplooimeting/pdf/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_MEDICAL, allow_read_only_get=True)(huidplooimeting_pdf), name="huidplooimeting_pdf"),


    # ---------- DATA ----------
    path("seed_data/", role_required(ROLE_ADMIN)(views.seed_data), name="seed_data"),
    path("player/<int:player_id>/data/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_MEDICAL, ROLE_TRAINER, allow_read_only_get=True)(views.player_data), name="player_data"),
    path("player/<int:player_id>/weights/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE, ROLE_MEDICAL, ROLE_TRAINER, allow_read_only_get=True)(views.weight_data), name="weight_data"),

    # ---------- UPLOAD ----------
    path("upload/", role_required(ROLE_ADMIN, ROLE_PERFORMANCE)(views.upload_file), name="upload_file"),
]

# ---------- MEDIA BESTANDEN ----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from main import views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ---------- BASIS ----------
    path("admin/", admin.site.urls),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.dashboard, name="home"),

    path("add_rehab/", views.add_rehab, name="add_rehab"),

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

    # ---------- DATA ----------
    path("seed_data/", views.seed_data, name="seed_data"),
    path("player/<int:player_id>/data/", views.player_data, name="player_data"),

    # ---------- UPLOAD ----------
    path("upload/", views.upload_file, name="upload_file"),
]

# ---------- MEDIA BESTANDEN ----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

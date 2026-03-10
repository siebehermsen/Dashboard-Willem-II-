from django.contrib import admin
from .models import DayProgramEntry, InjuryCase, PerformanceSession, Player, Staff


# ---------- SPELERS ----------
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "prev_weight_display", "curr_weight_display", "sum_skinfolds_display", "fat_perc_display", "weight_diff_display")
    search_fields = ("name",)
    list_filter = ()

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("monitoring_profile")

    def prev_weight_display(self, obj):
        return obj.monitoring_profile.prev_weight if getattr(obj, "monitoring_profile", None) else "-"

    def curr_weight_display(self, obj):
        return obj.monitoring_profile.curr_weight if getattr(obj, "monitoring_profile", None) else "-"

    def sum_skinfolds_display(self, obj):
        return obj.monitoring_profile.sum_skinfolds if getattr(obj, "monitoring_profile", None) else "-"

    def fat_perc_display(self, obj):
        return obj.monitoring_profile.fat_perc if getattr(obj, "monitoring_profile", None) else "-"

    def weight_diff_display(self, obj):
        profile = getattr(obj, "monitoring_profile", None)
        if not profile:
            return "-"
        if profile.prev_weight is None or profile.curr_weight is None:
            return "-"
        diff = round(profile.curr_weight - profile.prev_weight, 1)
        return diff if diff is not None else "-"

    prev_weight_display.short_description = "Vorig gewicht (kg)"
    curr_weight_display.short_description = "Huidig gewicht (kg)"
    sum_skinfolds_display.short_description = "Som huidplooien (mm)"
    fat_perc_display.short_description = "Vetpercentage (%)"
    weight_diff_display.short_description = "Verschil (kg)"


# ---------- REVALIDATIESPELERS ----------
@admin.register(InjuryCase)
class InjuryCaseAdmin(admin.ModelAdmin):
    list_display = ("player", "injury_type_display", "started_on", "expected_return_on", "status_display")
    search_fields = ("player__name", "injury_type_ref__name")
    list_filter = ("status_ref", "injury_type_ref", "phase_ref")

    def injury_type_display(self, obj):
        return obj.injury_type_ref.name if obj.injury_type_ref else "-"

    def status_display(self, obj):
        return obj.status_ref.code if obj.status_ref else "-"


# ---------- PERFORMANCE SESSIONS ----------
@admin.register(PerformanceSession)
class PerformanceSessionAdmin(admin.ModelAdmin):
    list_display = ("player", "session_kind_ref", "session_date", "week")
    search_fields = ("player__name",)
    list_filter = ("session_kind_ref", "week")


# ---------- WEEKPROGRAMMA ----------
@admin.register(DayProgramEntry)
class DayProgramEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "activities", "notes")
    search_fields = ("date", "activities", "notes")
    ordering = ("id",)

# ---------- STAFFLEDEN ----------
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("name", "role_ref")
    search_fields = ("name", "role_ref__name")
    ordering = ("name",)

from django.contrib import admin
from .models import Player, Injury, TrainingData, DayProgram, Staff


# ---------- SPELERS ----------
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "prev_weight", "curr_weight", "sum_skinfolds", "fat_perc", "weight_diff_display")
    search_fields = ("name",)
    list_filter = ("fat_perc",)

    def weight_diff_display(self, obj):
        diff = obj.weight_diff()
        return diff if diff is not None else "-"
    weight_diff_display.short_description = "Verschil (kg)"


# ---------- REVALIDATIESPELERS ----------
@admin.register(Injury)
class InjuryAdmin(admin.ModelAdmin):
    list_display = ("name", "injury_type", "duration", "start_date")
    search_fields = ("name", "injury_type")
    list_filter = ("injury_type",)


# ---------- TRAININGSDATA ----------
@admin.register(TrainingData)
class TrainingDataAdmin(admin.ModelAdmin):
    list_display = ("player", "week", "total_distance", "hsd", "sprints", "load")
    search_fields = ("player__name",)
    list_filter = ("week",)


# ---------- WEEKPROGRAMMA ----------
@admin.register(DayProgram)
class DayProgramAdmin(admin.ModelAdmin):
    list_display = ("date", "activities", "notes")
    search_fields = ("date", "activities", "notes")
    ordering = ("id",)

# ---------- STAFFLEDEN ----------
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("name", "role")
    search_fields = ("name", "role")
    ordering = ("name",)
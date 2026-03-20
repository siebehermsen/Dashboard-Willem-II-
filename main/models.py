from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime
import django

class AnthropometryMeasurement(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    category = models.CharField(choices=[('skinfold', 'Skinfold'), ('girth', 'Girth')], max_length=20)
    site_code = models.CharField(max_length=50)
    repetition = models.PositiveSmallIntegerField()
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='main.anthropometrysession')

    class Meta:
        ordering = ['category', 'site_code', 'repetition']
        indexes = [models.Index(fields=['category', 'site_code'], name='main_anthro_categor_c3426b_idx')]
        constraints = [models.UniqueConstraint(fields=('session', 'category', 'site_code', 'repetition'), name='uniq_anthro_measurement_per_rep')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class AnthropometrySession(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField()
    body_mass = models.FloatField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    fat_dw = models.FloatField(blank=True, null=True)
    fat_faulkner = models.FloatField(blank=True, null=True)
    fat_carter = models.FloatField(blank=True, null=True)
    fat_average = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anthropometry_sessions', to='main.player')

    class Meta:
        ordering = ['-date', '-id']
        constraints = [models.UniqueConstraint(fields=('player', 'date'), name='uniq_anthro_session_player_date')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class AttendanceRecord(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='main.player')
    status = models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='records', to='main.attendancestatus')

    class Meta:
        ordering = ['player__name', 'date']
        indexes = [models.Index(fields=['date', 'status'], name='main_attend_date_35e05c_idx')]
        constraints = [models.UniqueConstraint(fields=('player', 'date'), name='uniq_attendance_player_date')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class AttendanceStatus(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    code = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=100)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'label']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class BeweeganalyseBeoordeling(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    punt = models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='beoordelingen', to='main.beweeganalysepunt')
    sessie = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beoordelingen', to='main.beweeganalysesessie')
    priority_flag = models.BooleanField(default=False)

    class Meta:
        ordering = ['punt__onderdeel__sort_order', 'punt__sort_order', 'id']
        constraints = [models.UniqueConstraint(fields=('sessie', 'punt'), name='uniq_beweeganalyse_sessie_punt'), models.CheckConstraint(condition=models.Q(('score__isnull', True), models.Q(('score__gte', 1), ('score__lte', 4)), _connector='OR'), name='ck_beweeganalyse_score_1_4')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class BeweeganalyseOefening(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=255)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    punt = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oefeningen', to='main.beweeganalysepunt')

    class Meta:
        ordering = ['punt__onderdeel__sort_order', 'punt__sort_order', 'sort_order', 'id']
        constraints = [models.UniqueConstraint(fields=('punt', 'name'), name='uniq_beweeganalyse_oefening_punt_name')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class BeweeganalyseOnderdeel(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=120, unique=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class BeweeganalysePunt(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=80)
    focus_text = models.CharField(blank=True, default='', max_length=255)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    onderdeel = models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='punten', to='main.beweeganalyseonderdeel')

    class Meta:
        ordering = ['onderdeel__sort_order', 'sort_order', 'id']
        constraints = [models.UniqueConstraint(fields=('onderdeel', 'title', 'sort_order'), name='uniq_beweeganalyse_punt_template')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class BeweeganalyseSessie(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beweeganalyse_sessies', to='main.player')
    video_file = models.FileField(blank=True, null=True, upload_to='beweeganalyse_videos/')

    class Meta:
        ordering = ['-date', 'player__name']
        constraints = [models.UniqueConstraint(fields=('player', 'date'), name='uniq_beweeganalyse_sessie_player_date')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class BirthdayProfile(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    role = models.CharField(blank=True, choices=[('Speler', 'Speler'), ('Staf', 'Staf'), ('Overig', 'Overig')], max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=('name', 'role'), name='uniq_birthday_profile_name_role')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class BirthdayRecord(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='main.birthdayprofile')

    class Meta:
        ordering = ['date', 'profile__name']
        constraints = [models.UniqueConstraint(fields=('profile', 'date'), name='uniq_birthday_profile_date')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class DayProgramEntry(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField()
    title = models.CharField(blank=True, max_length=120, null=True)
    activities = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'id']
        constraints = [models.UniqueConstraint(fields=('date', 'title'), name='uniq_dayprogram_date_title')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class FieldRehabComponent(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class FieldRehabMetric(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    value = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metric_type = models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='metric_values', to='main.fieldrehabmetrictype')
    session = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='main.fieldrehabsession')

    class Meta:
        verbose_name = 'Veldrevalidatie metric'
        verbose_name_plural = 'Veldrevalidatie metrics'
        indexes = [models.Index(fields=['session', 'metric_type'], name='main_fieldr_session_143f39_idx'), models.Index(fields=['metric_type', 'value'], name='main_fieldr_metric__0a182e_idx')]
        constraints = [models.UniqueConstraint(fields=('session', 'metric_type'), name='uniq_fieldrehab_metric_per_session')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class FieldRehabMetricType(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(blank=True, max_length=20, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class FieldRehabPhase(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class FieldRehabSession(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    afgevinkt = models.BooleanField(default=False, verbose_name='Afgevinkt')
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.player', verbose_name='Speler')
    onderdeel_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sessions', to='main.fieldrehabcomponent', verbose_name='Onderdeel')
    phase_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sessions', to='main.fieldrehabphase', verbose_name='Revalidatiefase')

    class Meta:
        verbose_name = 'Veldrevalidatie sessie'
        verbose_name_plural = 'Veldrevalidatie sessies'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['player', 'created_at'], name='main_fieldr_player__292ad7_idx'), models.Index(fields=['phase_ref', 'onderdeel_ref'], name='main_fieldr_phase_r_edbaf4_idx')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class GrowthMeasurement(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField(verbose_name='Meetdatum')
    height_cm = models.FloatField(verbose_name='Lengte (cm)')
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='main.growthprofile')

    class Meta:
        verbose_name = 'Groeimeetpunt'
        verbose_name_plural = 'Groeimeetpunten'
        ordering = ['date', 'id']
        unique_together = (('profile', 'date'),)

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class GrowthProfile(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    age = models.FloatField(blank=True, null=True, verbose_name='Leeftijd (jaren)')
    height = models.FloatField(blank=True, null=True, verbose_name='Lengte (cm)')
    sitting_height = models.FloatField(blank=True, null=True, verbose_name='Zithoogte (cm)')
    weight = models.FloatField(blank=True, null=True, verbose_name='Gewicht (kg)')
    maturity_offset = models.FloatField(blank=True, null=True, verbose_name='Maturity offset')
    growth_complaints = models.BooleanField(default=False, verbose_name='Groeiklachten')
    action = models.CharField(blank=True, max_length=255, null=True, verbose_name='Actie')
    updated_at = models.DateTimeField(auto_now=True)
    player = models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='growth_profile', to='main.player')

    class Meta:
        verbose_name = 'Groeiprofiel'
        verbose_name_plural = 'Groeiprofielen'
        ordering = ['player__name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class HitAsrPlanEntry(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    mss_kmh = models.DecimalField(decimal_places=2, max_digits=5)
    mas_kmh = models.DecimalField(decimal_places=2, max_digits=5)
    target_speed_kmh = models.DecimalField(decimal_places=2, max_digits=6)
    asr_kmh = models.DecimalField(decimal_places=2, max_digits=5)
    pct_mas = models.DecimalField(decimal_places=2, max_digits=6)
    pct_asr = models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)
    indication = models.CharField(blank=True, max_length=40, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hit_asr_plan_entries', to='main.player')
    session = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='main.hitasrplansession')

    class Meta:
        verbose_name = 'HIT ASR planning regel'
        verbose_name_plural = 'HIT ASR planning regels'
        ordering = ['player__name']
        indexes = [models.Index(fields=['session', 'player'], name='main_hitasr_session_33b779_idx'), models.Index(fields=['player', 'created_at'], name='main_hitasr_player__061754_idx')]
        constraints = [models.UniqueConstraint(fields=('session', 'player'), name='uniq_hit_asr_plan_session_player')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class HitAsrPlanSession(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    session_date = models.DateField()
    mas_percent = models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Intensiteit (%MAS)')
    reference_speed_kmh = models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)
    notes = models.CharField(blank=True, max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'HIT ASR planning'
        verbose_name_plural = 'HIT ASR planningen'
        ordering = ['-session_date', '-created_at']
        indexes = [models.Index(fields=['session_date'], name='main_hitasr_session_3026b4_idx'), models.Index(fields=['created_at'], name='main_hitasr_created_9656eb_idx')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class HitWeekPlan(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(default='Algemene HIT Weekplanning', max_length=120)
    week_start = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trainer = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hit_week_plans', to=settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class HitWeekPlanEntry(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    day_of_week = models.PositiveSmallIntegerField(choices=[(1, 'Maandag'), (2, 'Dinsdag'), (3, 'Woensdag'), (4, 'Donderdag'), (5, 'Vrijdag'), (6, 'Zaterdag'), (7, 'Zondag')])
    content = models.CharField(blank=True, default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='main.hitweekplan')

    class Meta:
        ordering = ['day_of_week']
        constraints = [models.UniqueConstraint(fields=('plan', 'day_of_week'), name='uniq_hitplan_day')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class IndividualDayPlan(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='individual_day_plans', to='main.player')

    class Meta:
        ordering = ['-date', 'player__name']
        constraints = [models.UniqueConstraint(fields=('player', 'date'), name='uniq_individual_day_plan_player_date')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class IndividualDayPlanNote(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='main.individualdayplan')
    note_type_ref = models.ForeignKey(db_column='note_type_ref_id', on_delete=django.db.models.deletion.PROTECT, related_name='notes', to='main.individualdayplannotetype')

    class Meta:
        ordering = ['note_type_ref__code', 'id']
        constraints = [models.UniqueConstraint(fields=('plan', 'note_type_ref'), name='uniq_individual_day_plan_note_type')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class IndividualDayPlanNoteType(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class InjuryCase(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    started_on = models.DateField(blank=True, null=True)
    expected_return_on = models.DateField(blank=True, null=True)
    closed_on = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='injury_cases', to='main.player')
    injury_type_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='injury_cases', to='main.injurytype')
    phase_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='injury_cases', to='main.injuryphase')
    status_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='injury_cases', to='main.injurystatus')

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['started_on'], name='main_injury_started_738f54_idx'), models.Index(fields=['player', 'status_ref'], name='main_injury_player__503bda_idx')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class InjuryPhase(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class InjuryStatus(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    code = models.CharField(max_length=30, unique=True)
    label = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class InjuryType(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class Match(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    kickoff = models.DateTimeField()
    away_team = models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='away_matches', to='main.team')
    home_team = models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_matches', to='main.team')

    class Meta:
        ordering = ['kickoff']
        constraints = [models.UniqueConstraint(fields=('kickoff', 'home_team', 'away_team'), name='unique_match')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class NutritionDay(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    day = models.CharField(choices=[('Maandag', 'Maandag'), ('Dinsdag', 'Dinsdag'), ('Woensdag', 'Woensdag'), ('Donderdag', 'Donderdag'), ('Vrijdag', 'Vrijdag'), ('Zaterdag', 'Zaterdag'), ('Zondag', 'Zondag')], max_length=20, unique=True)
    meal = models.CharField(blank=True, max_length=255, null=True)
    color = models.CharField(blank=True, choices=[('red', 'Rood'), ('yellow', 'Geel'), ('green', 'Groen')], max_length=20, null=True)

    class Meta:
        pass

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class NutritionIntakeItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    meal_key = models.CharField(choices=[('breakfast', 'Ontbijt'), ('snack1', 'Snack 1'), ('lunch', 'Lunch'), ('snack2', 'Snack 2'), ('dinner', 'Diner'), ('snack3', 'Snack 3'), ('supplements', 'Supplementen')], max_length=30)
    value = models.CharField(blank=True, default='', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.nutritionintakesession')

    class Meta:
        ordering = ['meal_key']
        constraints = [models.UniqueConstraint(fields=('session', 'meal_key'), name='uniq_nutrition_item_per_meal')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class NutritionIntakeSession(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField(blank=True, null=True)
    goal = models.CharField(blank=True, max_length=255, null=True)
    next_meeting_goal = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nutrition_sessions', to='main.player')

    class Meta:
        ordering = ['-date', '-updated_at', '-id']
        indexes = [models.Index(fields=['player', 'date'], name='main_nutrit_player__b27b72_idx')]
        constraints = [models.UniqueConstraint(fields=('player', 'date'), name='uniq_nutri_session_player_date')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class Oefening(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    player = models.ForeignKey(blank=True, db_column='player_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='main.player')
    exercise = models.CharField(blank=True, max_length=150, null=True, verbose_name='Oefening')
    description = models.TextField(blank=True, null=True, verbose_name='Beschrijving')
    sets_reps = models.CharField(blank=True, max_length=50, null=True, verbose_name='Sets / Herhalingen')
    created_at = models.DateTimeField(default=django.utils.timezone.now, verbose_name='Datum toegevoegd')
    focus_point_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='oefeningen', to='main.oefeningfocuspoint', verbose_name='Aandachtspunt')
    phase_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='oefeningen', to='main.oefeningphase', verbose_name='Fase')
    program_type_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='oefeningen', to='main.oefeningprogramtype', verbose_name='Programmatype')

    class Meta:
        verbose_name = 'Oefening'
        verbose_name_plural = 'Oefeningen'
        ordering = ['player', '-created_at']
        indexes = [models.Index(fields=['program_type_ref', 'phase_ref'], name='main_oefeni_program_6fa76b_idx')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class OefeningFocusPoint(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class OefeningPhase(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class OefeningProgramType(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class OverigNote(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    note_type = models.CharField(choices=[('note', 'Vrije notitie'), ('section', 'Sectietekst')], default='note', max_length=20)
    page_key = models.CharField(blank=True, max_length=50, null=True)
    section_key = models.CharField(blank=True, max_length=50, null=True)
    text = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']
        indexes = [models.Index(fields=['note_type', 'page_key', 'section_key'], name='main_overig_note_ty_12667b_idx'), models.Index(fields=['created_at'], name='main_overig_created_a44713_idx')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class PerformanceMetric(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    metric_type = models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='values', to='main.performancemetrictype')
    session = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='main.performancesession')

    class Meta:
        ordering = ['session_id', 'metric_type__code']
        indexes = [models.Index(fields=['metric_type', 'value'], name='main_perfor_metric__11adaa_idx')]
        constraints = [models.UniqueConstraint(fields=('session', 'metric_type'), name='uniq_perf_metric_per_session_type')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class PerformanceMetricType(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=120)
    unit = models.CharField(blank=True, default='', max_length=30)
    category = models.CharField(blank=True, default='', max_length=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'label']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class PerformanceSession(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    session_date = models.DateField()
    week = models.PositiveIntegerField(blank=True, null=True)
    source_legacy_table = models.CharField(blank=True, max_length=50, null=True)
    source_legacy_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_sessions', to='main.player')
    session_kind_ref = models.ForeignKey(db_column='session_kind_ref_id', on_delete=django.db.models.deletion.PROTECT, related_name='sessions', to='main.performancesessionkind')

    class Meta:
        ordering = ['-session_date', 'player__name', 'session_kind_ref__code']
        indexes = [models.Index(fields=['player', 'session_date'], name='main_perfor_player__4b4079_idx'), models.Index(fields=['session_kind_ref', 'session_date'], name='main_perfor_session_f2abd8_idx')]
        constraints = [models.UniqueConstraint(fields=('player', 'session_kind_ref', 'session_date', 'source_legacy_table', 'source_legacy_id'), name='uniq_perf_session_per_source')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class PerformanceSessionKind(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['label']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class Player(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, verbose_name='Naam speler')
    image = models.ImageField(blank=True, null=True, upload_to='player_images/', verbose_name='Profielfoto')
    position_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='players', to='main.playerposition', verbose_name='Positie')

    class Meta:
        pass

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class PlayerMonitoringProfile(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    prev_weight = models.FloatField(blank=True, null=True, verbose_name='Vorig gewicht (kg)')
    curr_weight = models.FloatField(blank=True, null=True, verbose_name='Huidig gewicht (kg)')
    sum_skinfolds = models.FloatField(blank=True, null=True, verbose_name='Som huidplooien (mm)')
    fat_perc = models.FloatField(blank=True, null=True, verbose_name='Vetpercentage (%)')
    nutrition_focus = models.TextField(blank=True, help_text="Bijv. 'Meer ontbijt eten', 'Extra herstelshake nemen na training', etc.", null=True, verbose_name='Voedingsaandachtspunt')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player = models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='monitoring_profile', to='main.player')

    class Meta:
        ordering = ['player__name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class PlayerPosition(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class PlayerSpeedTest(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    test_date = models.DateField()
    mss_kmh = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='MSS (km/u)')
    mas_kmh = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='MAS (km/u)')
    notes = models.CharField(blank=True, max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speed_tests', to='main.player')

    class Meta:
        verbose_name = 'Snelheidstest (MSS/MAS)'
        verbose_name_plural = 'Snelheidstesten (MSS/MAS)'
        ordering = ['-test_date', 'player__name']
        indexes = [models.Index(fields=['player', 'test_date'], name='main_player_player__54dc7a_idx'), models.Index(fields=['test_date'], name='main_player_test_da_19ee67_idx')]
        constraints = [models.UniqueConstraint(fields=('player', 'test_date'), name='uniq_speed_test_player_date'), models.CheckConstraint(condition=models.Q(('mss_kmh__gt', 0)), name='ck_speedtest_mss_pos'), models.CheckConstraint(condition=models.Q(('mas_kmh__gt', 0)), name='ck_speedtest_mas_pos')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class PlayerTeamAssignment(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_assignments', to='main.player')
    team = models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='player_assignments', to='main.team')

    class Meta:
        ordering = ['-start_date', 'player__name']
        constraints = [models.UniqueConstraint(fields=('player', 'team', 'start_date'), name='uniq_player_team_start')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class Programma(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    doel = models.CharField(blank=True, max_length=255, null=True, verbose_name='Doel')
    sterke_punten = models.TextField(blank=True, null=True, verbose_name='Sterke punten')
    verbeterpunten = models.TextField(blank=True, null=True, verbose_name='Verbeterpunten')
    plan_komende_periode = models.TextField(blank=True, null=True, verbose_name='Plan komende periode')
    video_links = models.TextField(blank=True, null=True, verbose_name='Videolinks')
    fysiek_ontwikkelpunt = models.TextField(blank=True, null=True, verbose_name='Fysiek ontwikkelpunt')
    ontwikkelaanpak = models.TextField(blank=True, null=True, verbose_name='Hoe gaat de speler dit ontwikkelen')
    evaluatie_datum = models.DateField(blank=True, null=True, verbose_name='Evaluatiedatum')
    created_at = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.player', verbose_name='Speler')

    class Meta:
        verbose_name = 'Individueel Programma'
        verbose_name_plural = "Individuele Programma's"
        ordering = ['-created_at']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class ProgrammaDuurUnit(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class ProgrammaFrequentie(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class ProgrammaOefening(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    opmerkingen = models.TextField(blank=True, null=True)
    programma = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oefeningen', to='main.programma')
    frequentie_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='oefeningen', to='main.programmafrequentie')
    rpe_value = models.PositiveSmallIntegerField(blank=True, null=True)
    duur_text_override = models.CharField(blank=True, max_length=50, null=True)
    duur_unit_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='oefeningen', to='main.programmaduurunit')
    duur_value = models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)
    naam_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='programma_oefeningen', to='main.programmaoefeningnaam')

    class Meta:
        verbose_name = 'Programma Oefening'
        verbose_name_plural = 'Programma Oefeningen'

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class ProgrammaOefeningNaam(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class RPEEntry(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField()
    rpe = models.IntegerField(verbose_name='RPE (1ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ10)')
    session_load = models.IntegerField(blank=True, null=True, verbose_name='Sessie Load (optioneel)')
    created_at = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.player')
    training_type_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='main.rpetrainingtype', verbose_name='Trainingstype')

    class Meta:
        verbose_name = 'RPE Invoer'
        verbose_name_plural = 'RPE Registraties'
        ordering = ['-date', 'player']
        indexes = [models.Index(fields=['date', 'player'], name='main_rpeent_date_fbec02_idx')]
        constraints = [models.UniqueConstraint(fields=('player', 'date'), name='uniq_rpe_player_date'), models.CheckConstraint(condition=models.Q(('rpe__gte', 1), ('rpe__lte', 10)), name='ck_rpe_between_1_10'), models.CheckConstraint(condition=models.Q(('session_load__isnull', True), ('session_load__gte', 0), _connector='OR'), name='ck_rpe_session_load_nonneg')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class RPETrainingType(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class Staff(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    role_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='staff_members', to='main.staffrole')

    class Meta:
        verbose_name = 'Staflid'
        verbose_name_plural = 'Stafleden'
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class StaffRole(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class Team(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class VakantiePlanning(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField(verbose_name='Datum')
    loopvorm = models.CharField(blank=True, max_length=255, null=True, verbose_name='Loopvorm')
    kracht = models.CharField(blank=True, max_length=255, null=True, verbose_name='Kracht')
    visible_from = models.DateField(verbose_name='Zichtbaar vanaf')
    is_visible = models.BooleanField(default=False, verbose_name='Zichtbaar')
    created_at = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(related_name='vakantie_planningen', to='main.player', verbose_name='Spelers')

    class Meta:
        verbose_name = 'Vakantieplanning'
        verbose_name_plural = 'Vakantieplanningen'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class VakantieProgrammaEntry(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField(verbose_name='Datum')
    loopvorm = models.CharField(blank=True, max_length=255, null=True, verbose_name='Loopvorm')
    kracht = models.CharField(blank=True, max_length=255, null=True, verbose_name='Kracht')
    completed = models.BooleanField(default=False, verbose_name='Uitgevoerd')
    created_at = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.player', verbose_name='Speler')

    class Meta:
        verbose_name = 'Vakantieprogramma item'
        verbose_name_plural = 'Vakantieprogramma items'
        ordering = ['-date', 'player']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')


class TrainingWeekTarget(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(default='Geplande weektargets training', max_length=120)
    monday = models.CharField(blank=True, default='', max_length=255, verbose_name='Maandag')
    tuesday = models.CharField(blank=True, default='', max_length=255, verbose_name='Dinsdag')
    wednesday = models.CharField(blank=True, default='', max_length=255, verbose_name='Woensdag')
    thursday = models.CharField(blank=True, default='', max_length=255, verbose_name='Donderdag')
    friday = models.CharField(blank=True, default='', max_length=255, verbose_name='Vrijdag')
    saturday = models.CharField(blank=True, default='', max_length=255, verbose_name='Zaterdag')
    sunday = models.CharField(blank=True, default='', max_length=255, verbose_name='Zondag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Training weektarget'
        verbose_name_plural = 'Training weektargets'
        ordering = ['-updated_at']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class WeightEntry(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField()
    weight = models.FloatField()
    player = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weights', to='main.player')

    class Meta:
        ordering = ['-date']
        unique_together = (('player', 'date'),)
        constraints = [models.CheckConstraint(condition=models.Q(('weight__gt', 0)), name='ck_weight_pos')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class WellnessEntry(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField(verbose_name='Datum')
    sleep = models.IntegerField(blank=True, null=True, verbose_name='Hoe heb je geslapen? (1ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ5)')
    mood = models.IntegerField(blank=True, null=True, verbose_name='Hoe voel je je? (1ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ5)')
    fitness = models.IntegerField(blank=True, null=True, verbose_name='Voel je je fit? (1ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ5)')
    soreness = models.IntegerField(blank=True, null=True, verbose_name='Spierpijn? (1ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ5)')
    comment = models.TextField(blank=True, null=True, verbose_name='Opmerkingen')
    player = models.ForeignKey(db_column='player_id', on_delete=django.db.models.deletion.CASCADE, to='main.player', verbose_name='Speler')

    class Meta:
        verbose_name = 'Wellnessinvoer'
        verbose_name_plural = 'Wellnessdata'
        ordering = ['-date', 'player']
        indexes = [models.Index(fields=['date', 'player'], name='main_wellne_date_cc439a_idx')]
        constraints = [models.UniqueConstraint(fields=('player', 'date'), name='uniq_wellness_player_date'), models.CheckConstraint(condition=models.Q(('sleep__isnull', True), models.Q(('sleep__gte', 1), ('sleep__lte', 5)), _connector='OR'), name='ck_well_sleep_1_5'), models.CheckConstraint(condition=models.Q(('mood__isnull', True), models.Q(('mood__gte', 1), ('mood__lte', 5)), _connector='OR'), name='ck_well_mood_1_5'), models.CheckConstraint(condition=models.Q(('fitness__isnull', True), models.Q(('fitness__gte', 1), ('fitness__lte', 5)), _connector='OR'), name='ck_well_fit_1_5'), models.CheckConstraint(condition=models.Q(('soreness__isnull', True), models.Q(('soreness__gte', 1), ('soreness__lte', 5)), _connector='OR'), name='ck_well_sore_1_5')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class YouthGuestProfile(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    team_ref = models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profiles', to='main.youthguestteam')

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(fields=('name', 'team_ref'), name='uniq_youthguest_profile_name_team_ref')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class YouthGuestTeam(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')

class YouthGuestWeek(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    week_of = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weeks', to='main.youthguestprofile')

    class Meta:
        ordering = ['-week_of', 'profile__name']
        constraints = [models.UniqueConstraint(fields=('profile', 'week_of'), name='uniq_youthguest_profile_week')]

    def __str__(self):
        return getattr(self, 'name', f'{self.__class__.__name__} {self.pk}')


from django.db.models import Count
from django.db.models.functions import Extract

from .models import Clinic, Department, Doctor, Room, Patient, Appointment, MedicalRecord, Comment, DoctorSchedule

from django.contrib import admin


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'medical_history', 'get_total_patients', 'get_new_patients', 'get_gender_distribution', 'get_birth_year_distribution')
    list_filter = ('user__gender',)
    search_fields = ('user__username',)

    def get_total_patients(self, obj):
        return Patient.objects.count()
    get_total_patients.short_description = 'Total Patients'

    def get_new_patients(self, obj):
        from datetime import datetime, timedelta
        start_date = datetime.now() - timedelta(days=30)
        return Patient.objects.filter(user__date_joined__gte=start_date).count()
    get_new_patients.short_description = 'New Patients (last 30 days)'

    def get_gender_distribution(self, obj):
        return Patient.objects.values('user__gender').annotate(count=Count('id'))
    get_gender_distribution.short_description = 'Gender Distribution'

    def get_birth_year_distribution(self, obj):
        return Patient.objects.annotate(birth_year=Extract('user__birth_date', 'year')).values('birth_year').annotate(count=Count('id')).order_by('birth_year')
    get_birth_year_distribution.short_description = 'Birth Year Distribution'


admin.site.register(Clinic)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Room)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Comment)
admin.site.register(DoctorSchedule)
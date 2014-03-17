from django.contrib import admin
from obpacient.models import patient

# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display = ('p_name', 'p_code', 'p_age', 'p_LMP', 'p_EDC', 'p_conception')
    search_fields = ('p_name', 'p_LMP', 'p_EDC')
    list_filter = ('p_name', 'p_LMP', 'p_EDC')
    date_hierarchy = 'p_EDC'

admin.site.register(patient, PatientAdmin)
from django.contrib import admin
from .models import Lookup, PersonalCare, HealthCareProvider

@admin.register(Lookup)
class LookupAdmin(admin.ModelAdmin):
    list_display = ('id', 'lookup_label', 'lookup_type', 'lookup_value', 'created_at', 'updated_at')
    search_fields = ('lookup_label', 'lookup_type', 'lookup_value')
    list_filter = ('lookup_type', 'created_at')
    ordering = ('-created_at',)

@admin.register(HealthCareProvider)
class HealthCareProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'service_type', 'email', 'contact_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'HPR_ID')
    list_filter = ('service_type', 'gender', 'created_at')
    ordering = ('-created_at',)

@admin.register(PersonalCare)
class PersonalCareAdmin(admin.ModelAdmin):
    list_display = ('healthcare_provider_id', 'personal_care_type', 'experience', 'price_rate', 'created_at')
    search_fields = ('personal_care_type', 'experience')
    list_filter = ('personal_care_type', 'created_at')
    ordering = ('-created_at',)
from django.contrib import admin
from .models import (
    HealthRecord,
    Rating,
    PersonalCareService,
    Appointment,
    MedicalHistory,
)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_type', 'sample_collection', 'uploaded_by', 'checked_by', 'is_active')
    search_fields = ('user__username', 'report_type', 'uploaded_by', 'checked_by')
    list_filter = ('report_type', 'sample_collection', 'is_active', 'is_deleted')
    ordering = ('-sample_collection',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ("Basic Information", {
            'fields': ('user', 'file', 'report_type')
        }),
        ("Details", {
            'fields': ('sample_collection', 'uploaded_by', 'checked_by')
        }),
        ("Status", {
            'fields': ('is_active', 'is_deleted')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('healthcare_provider', 'patient', 'rating', 'review', 'review_date', 'is_active', 'created_at')
    search_fields = ('healthcare_provider__name', 'review', 'patient__user__first_name', 'patient__user__last_name')
    list_filter = ('rating', 'is_active', 'is_deleted', 'review_date')
    ordering = ('-rating', '-review_date')
    readonly_fields = ('created_at', 'updated_at', 'review_date')

    fieldsets = (
        ("Rating Information", {
            'fields': ('healthcare_provider', 'patient', 'rating', 'review', 'review_date')
        }),
        ("Status", {
            'fields': ('is_active', 'is_deleted')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PersonalCareService)
class PersonalCareServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'price', 'availability', 'is_active')
    search_fields = ('name', 'provider__username', 'description')
    list_filter = ('availability', 'is_active', 'is_deleted')
    ordering = ('name', '-created_at')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Service Information", {
            'fields': ('provider', 'name', 'description', 'price')
        }),
        ("Media", {
            'fields': ('image',)
        }),
        ("Status", {
            'fields': ('availability', 'is_active', 'is_deleted')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'healthcare_provider', 'service', 'appointment_date', 'status', 'is_active')
    search_fields = ('patient__username', 'healthcare_provider__name', 'service__name')
    list_filter = ('status', 'appointment_date', 'is_active', 'is_deleted')
    ordering = ('appointment_date', '-created_at')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Appointment Information", {
            'fields': ('patient', 'healthcare_provider', 'service', 'appointment_date')
        }),
        ("Details", {
            'fields': ('status', 'notes')
        }),
        ("Status", {
            'fields': ('is_active', 'is_deleted')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'condition', 'diagnosis_date', 'severity', 'is_ongoing', 'is_active')
    search_fields = ('patient__username', 'condition', 'symptoms', 'treatment')
    list_filter = ('condition', 'severity', 'is_ongoing', 'is_active', 'is_deleted')
    ordering = ('-diagnosis_date', '-created_at')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Patient Information", {
            'fields': ('patient', 'healthcare_provider')
        }),
        ("Condition Details", {
            'fields': ('condition', 'diagnosis_date', 'severity', 'is_ongoing')
        }),
        ("Medical Information", {
            'fields': ('symptoms', 'treatment', 'medications')
        }),
        ("Status", {
            'fields': ('is_active', 'is_deleted')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

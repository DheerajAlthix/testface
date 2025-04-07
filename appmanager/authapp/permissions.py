from rest_framework import permissions
from django.shortcuts import get_object_or_404
from appmanager.doctor.models import HealthCareProvider
from appmanager.patient.models import Patient

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   HealthCareProvider.objects.filter(user=request.user).exists())

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   Patient.objects.filter(user=request.user).exists())

class IsStaffOrDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   (request.user.is_staff or HealthCareProvider.objects.filter(user=request.user).exists()))

class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user

class IsDoctorOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False 
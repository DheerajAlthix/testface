from django.contrib import admin
from .models import UserProfile,ABHAUser, OTPRequest



admin.site.register(UserProfile)
admin.site.register(ABHAUser)
admin.site.register(OTPRequest)
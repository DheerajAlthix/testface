from django.db import models

class ABHAUser(models.Model):
    client_id = models.CharField(max_length=255, unique=True)
    client_secret = models.CharField(max_length=255)
    access_token = models.CharField(max_length=512, blank=True, null=True)
    refresh_token = models.CharField(max_length=512, blank=True, null=True)
    txn_id = models.CharField(max_length=255, blank=True, null=True)
    abha_number = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_id} - {self.abha_number or 'No ABHA'}"

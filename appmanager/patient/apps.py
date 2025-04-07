from django.apps import AppConfig
import os 

class PatientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = f"{os.environ.get('parent_folder')}.patient"

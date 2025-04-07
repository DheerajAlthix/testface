
import os
from django.contrib import admin
from django.urls import path,include

# f"{os.environ.get('parent_folder')}.patient"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(f"{os.environ.get('parent_folder')}.authapp.urls")),
    path('api/patient/', include(f"{os.environ.get('parent_folder')}.patient.urls")),
    path('api/doctor/', include(f"{os.environ.get('parent_folder')}.doctor.urls")),
]
        
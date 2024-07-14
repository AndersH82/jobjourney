from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("resume/", include("resume.urls")),
    path("admin/", admin.site.urls),
]
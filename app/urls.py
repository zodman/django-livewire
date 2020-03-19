from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("livewire.urls")),
    path('', index),
] + staticfiles_urlpatterns()

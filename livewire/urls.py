
from django.urls import path
from .views import livewire_message

urlpatterns = [
    path('livewire/message/<component_name>', livewire_message, name='livewire_app_url'),
]


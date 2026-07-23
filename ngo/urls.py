from django.urls import path
from .views import MyNGOProfileView, NGOProfileCreateView

urlpatterns = [
    path('ngo-profile/', MyNGOProfileView.as_view(), name='my-ngo-profile'),
    path('ngo-profile/create/', NGOProfileCreateView.as_view(), name='create-ngo-profile'),
]
from django.urls import path
from . import views 
from app_regulation.views import send_manual_email

urlpatterns = [
    path('regulations/', views.regulation_list, name='regulation_list'),
    path('manualmail/', views.regulations_manualmail, name='regulations_manualmail'),
    path('regulation-send-email/<int:country_id>/', send_manual_email, name='regulation_manual_email'),
]

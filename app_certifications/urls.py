from django.urls import path
from . import views
from .views import send_manual_email , trigger_weekly_email


urlpatterns = [
    path('listview/', views.listview, name='listview'),  # เพิ่ม '/' ท้ายเส้นทางนี้ให้ชัดเจน
    path('country_list/', views.country_list, name='country_list'),  # แก้ไขให้ตรงกัน
    path('certification_list/<str:country_name>/', views.certification_list, name='certification_list'),
    path('send-email/<int:country_id>/', send_manual_email, name='send_manual_email'),
    path('trigger-weekly-email/', trigger_weekly_email, name='trigger-weekly-email'),

    # URLs ด้านล่างนี้ควรอยู่หลัง listview เพื่อป้องกันไม่ให้จับ URL ผิดพลาด
    path('<str:country_name>/', views.certifications_by_country, name='certifications_by_country'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('minstandardtest/', views.minstandardtest_view, name='min_standard_test'),
    
]

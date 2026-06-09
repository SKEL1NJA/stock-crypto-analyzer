from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard_default'),
    
    path('secret-cron-trigger-998877/', views.trigger_update, name='trigger_update'),

    path('asset/<str:symbol>/', views.dashboard, name='dashboard_symbol'),
    path('<str:symbol>/', views.dashboard, name='dashboard_symbol_fallback'),
]
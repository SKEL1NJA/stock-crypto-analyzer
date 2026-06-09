from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard_default'),
    path('<str:symbol>/', views.dashboard, name='dashboard_symbol'),
]
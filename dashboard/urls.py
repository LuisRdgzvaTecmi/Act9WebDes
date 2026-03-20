from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

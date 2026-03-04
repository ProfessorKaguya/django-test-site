from django.urls import path
from . import views

urlpatterns = [
    path('reg/', views.register, name='reg'),
    path('profile', views.profile, name='profile'),
]
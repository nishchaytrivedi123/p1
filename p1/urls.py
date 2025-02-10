"""p1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="home"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('update-rsvp/', views.update_rsvp, name='update_rsvp'),
    path('create-family-guest/', views.create_family_and_guest, name='create_family_and_guest'),
    path('view-guests/', views.view_guests, name='view_guests'),
    path('generate_excel/', views.generate_excel, name='generate_excel'),
]

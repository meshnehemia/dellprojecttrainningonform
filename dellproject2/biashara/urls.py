
from django.contrib import admin
from django.urls import path
from biashara import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register, name='register'),
]

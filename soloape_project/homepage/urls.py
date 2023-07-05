from . import views

from django.urls import path


app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='index'),
]

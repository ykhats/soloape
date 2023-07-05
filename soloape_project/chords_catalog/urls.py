from django.urls import path

from . import views

app_name = 'chords_catalog'

urlpatterns = [
    path('', views.chords_list, name='chords_list'),
    path('<str:chord_name>/', views.chord_detail, name='chord_detail'),
]

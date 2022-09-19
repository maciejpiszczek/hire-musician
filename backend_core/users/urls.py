from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.MusiciansProfilesListView.as_view(), name='musicians_list'),
    path('<slug:slug>/', views.MusicianProfileView.as_view(), name='profile_details'),
]

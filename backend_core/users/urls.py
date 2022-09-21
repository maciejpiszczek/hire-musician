from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.MusiciansProfilesListView.as_view(), name='musicians_list'),
    path('login/', views.login_user_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.registration_view, name='registration'),
    path('<slug:slug>/', views.MusicianProfileView.as_view(), name='profile_details'),
    path('<slug:slug>/edit/', views.EditProfileView.as_view(), name='edit_profile'),
]

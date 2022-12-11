from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.MusiciansProfilesListView.as_view(), name='musicians_list'),
    path('login/', views.login_user_view, name='login'),
    path('register/', views.registration_view, name='registration'),
    path('profile/<slug:slug>/', views.MusicianProfileView.as_view(), name='profile_details'),
    path('<slug:slug>/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('password_change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('password_change/done/', views.ChangePasswordDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset/done/', views.ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/', views.ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
]
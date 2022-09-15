from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', views.UserProfileView.as_view(), name='profile_details'),
]

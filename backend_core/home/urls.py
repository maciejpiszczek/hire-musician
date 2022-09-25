from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.search, name='search'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
]

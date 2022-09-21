from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobsListView.as_view(), name='jobs_list'),
    path('<slug:slug>', views.JobDetailView.as_view(), name='job_details'),
    path('studiosession/new/', views.CreateStudioSessionView.as_view(), name='new_session'),
    path('concert/new/', views.CreateConcertView.as_view(), name='new_concert'),
    path('tour/new/', views.CreateTourView.as_view(), name='new_tour'),
]

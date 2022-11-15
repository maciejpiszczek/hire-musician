from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobsListView.as_view(), name='jobs_list'),
    path('view/<slug:slug>/', views.JobDetailView.as_view(), name='job_details'),
    path('studiosession/new/', views.CreateStudioSessionView.as_view(), name='new_session'),
    path('concert/new/', views.CreateConcertView.as_view(), name='new_concert'),
    path('tour/new/', views.CreateTourView.as_view(), name='new_tour'),
    path('studiosession/edit/<slug:slug>/', views.EditStudioSessionView.as_view(), name='edit_session'),
    path('concert/edit/<slug:slug>/', views.EditConcertView.as_view(), name='edit_concert'),
    path('tour/edit/<slug:slug>/', views.EditTourView.as_view(), name='edit_tour'),
    path('apply/<slug:slug>/', views.JobAccessView.as_view(), name='apply'),
    path('my/', views.MyJobsListView.as_view(), name='my_jobs'),
    path('my_accesses/', views.MyJobAccessesListView.as_view(), name='my_accesses'),
    path('delete/<slug:slug>/', views.JobDeleteView.as_view(), name='delete-job'),
]

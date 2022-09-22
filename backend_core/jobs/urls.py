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
    path('my/', views.MyJobsListView.as_view(), name='my_jobs'),
    path('studiosession/delete/<slug:slug>/', views.StudioSessionDeleteView.as_view(), name='delete_session'),
    path('concert/delete/<slug:slug>/', views.ConcertDeleteView.as_view(), name='delete_concert'),
    path('tour/delete/<slug:slug>/', views.TourDeleteView.as_view(), name='delete_tour'),
    path('apply_studiosession/<slug:slug>/', views.StudioSessionAccessView.as_view(), name='apply_session'),
    path('apply_concert/<slug:slug>/', views.ConcertAccessView.as_view(), name='apply_concert'),
    path('apply_tour/<slug:slug>/', views.TourAccessView.as_view(), name='apply_tour'),
]

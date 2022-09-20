from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobsListView.as_view(), name='jobs_list'),
    path('<slug:slug>', views.JobDetailView.as_view(), name='job_details'),
    path('new_session/', views.CreateStudioSessionView.as_view(), name='new_session'),
]

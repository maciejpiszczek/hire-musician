from django.urls import path

from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.MessagesListView.as_view(), name='list'),
    path('new/', views.NewMessageView.as_view(), name='new_message'),
]

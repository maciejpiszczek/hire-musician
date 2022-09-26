from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat-view'),
    path('<str:room_name>/', views.room_view, name='chat-view'),
]

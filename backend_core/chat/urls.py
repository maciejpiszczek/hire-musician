from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat-view'),
    path('<int:pk>/', views.ChatRoomView.as_view(), name='room-view'),
]

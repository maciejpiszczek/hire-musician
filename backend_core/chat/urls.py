from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatIndexView.as_view(), name='chat-index'),
    path('<int:pk>/', views.ChatRoomView.as_view(), name='chat-view'),
]

from django.urls import path

from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.ConversationsListView.as_view(), name='conversations-list'),
    path('new/', views.NewMessageView.as_view(), name='new-message'),
    path('conversation/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation'),
]

# path('messages/', views.MessagesListView.as_view(), name='messages-list'),
# path('<pk>/msg/', views.NewMessageInThreadView.as_view(), name='new-msg-thread'),
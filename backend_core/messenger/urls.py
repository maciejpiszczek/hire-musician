from django.urls import path

from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.ConversationsListView.as_view(), name='conversations-list'),
    path('new/', views.NewMessageView.as_view(), name='new-message'),
    path('new/<int:pk>/', views.NewPersonalMessageView.as_view(), name='personal-message'),
    path('conversation/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation'),
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('outbox/', views.OutboxView.as_view(), name='outbox'),
]

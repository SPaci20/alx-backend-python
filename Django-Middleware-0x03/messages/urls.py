from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.MessageListCreateView.as_view(), name='message-list'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
    path('messages/user/<str:username>/', views.UserMessagesView.as_view(), name='user-messages'),
    path('messages/user/<str:username>/unread/', views.UnreadMessagesView.as_view(), name='unread-messages'),
]
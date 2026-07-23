from django.urls import path
from .views import NotificationListView, MarkNotificationReadView, UnreadCountView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
    path('notifications/unread-count/', UnreadCountView.as_view(), name='notification-unread-count'),
]
# tasks/urls.py
from django.urls import path
from .views import TaskListView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
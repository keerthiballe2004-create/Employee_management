from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, tasks_page

router = DefaultRouter()

router.register(
    r'tasks',
    TaskViewSet,
    basename='tasks'
)

urlpatterns = [
    path('tasks/ui/', tasks_page, name='tasks_page'),
] + router.urls
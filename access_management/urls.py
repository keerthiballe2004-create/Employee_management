from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AccessViewSet, access_page

router = DefaultRouter()

urlpatterns = [
    path('access/ui/', access_page, name='access_page'),
]

router.register(
    r'access',
    AccessViewSet,
    basename='access'
)

urlpatterns += router.urls
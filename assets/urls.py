from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AssetViewSet,
    AssetAssignmentViewSet,
    assets_page
)

router = DefaultRouter()

urlpatterns = [
    path('assets/ui/', assets_page, name='assets_page'),
]

router.register('assets', AssetViewSet, basename='assets')
router.register(
    'asset-assignments',
    AssetAssignmentViewSet,
    basename='asset-assignments'
)

urlpatterns += router.urls
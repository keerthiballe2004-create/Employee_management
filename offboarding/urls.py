from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OffboardingCaseViewSet, offboarding_page

router = DefaultRouter()

router.register(
    r'offboarding',
    OffboardingCaseViewSet,
    basename='offboarding'
)

urlpatterns = [
    path('offboarding/ui/', offboarding_page, name='offboarding_page'),
] + router.urls
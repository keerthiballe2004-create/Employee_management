
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import OnboardingCaseViewSet, onboarding_page

router = DefaultRouter()

router.register(
    r'onboarding',
    OnboardingCaseViewSet,
    basename='onboarding'
)

urlpatterns = [
    path('onboarding/ui/', onboarding_page, name='onboarding_page'),
] + router.urls

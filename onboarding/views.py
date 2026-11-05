
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import OnboardingCase
from .serializers import OnboardingCaseSerializer


class OnboardingCaseViewSet(viewsets.ModelViewSet):

    queryset = OnboardingCase.objects.select_related('employee').all()

    serializer_class = OnboardingCaseSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = ['status', 'start_date', 'employee']

    search_fields = [
        'onboarding_id',
        'employee__first_name',
        'employee__last_name'
    ]

    ordering_fields = ['start_date', 'created_at']


@ensure_csrf_cookie
def onboarding_page(request):
    return render(request, 'onboarding.html')

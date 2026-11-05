from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import OffboardingCase
from .serializers import OffboardingCaseSerializer


class OffboardingCaseViewSet(viewsets.ModelViewSet):

    queryset = OffboardingCase.objects.select_related('employee').all()

    serializer_class = OffboardingCaseSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = ['status', 'exit_date', 'employee']

    search_fields = [
        'offboarding_id',
        'employee__first_name',
        'employee__last_name',
        'reason'
    ]

    ordering_fields = ['exit_date', 'created_at']


@ensure_csrf_cookie
def offboarding_page(request):
    return render(request, 'offboarding.html')
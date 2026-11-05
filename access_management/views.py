from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Access
from .serializers import AccessSerializer


class AccessViewSet(viewsets.ModelViewSet):

    queryset = Access.objects.select_related('employee').all()
    serializer_class = AccessSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = [
        'status',
        'system_name',
        'access_level',
        'employee'
    ]

    search_fields = [
        'access_id',
        'system_name',
        'access_level',
        'requested_by',
        'employee__first_name',
        'employee__last_name'
    ]

    ordering_fields = [
        'requested_date',
        'approved_date',
        'created_at'
    ]


@ensure_csrf_cookie
def access_page(request):
    return render(request, 'access.html')
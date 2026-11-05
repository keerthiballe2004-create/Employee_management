from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Asset, AssetAssignment
from .serializers import AssetSerializer, AssetAssignmentSerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = ['asset_type', 'status']
    search_fields = ['asset_id', 'asset_name', 'serial_number']
    ordering_fields = ['purchase_date', 'asset_name']


class AssetAssignmentViewSet(viewsets.ModelViewSet):
    queryset = AssetAssignment.objects.select_related(
        'asset', 'employee'
    ).all()

    serializer_class = AssetAssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = ['employee', 'asset', 'is_returned']
    search_fields = [
        'assignment_id',
        'employee__first_name',
        'employee__last_name',
        'asset__asset_name'
    ]

    ordering_fields = ['assigned_date', 'returned_date']


@ensure_csrf_cookie
def assets_page(request):
    return render(request, 'assets.html')
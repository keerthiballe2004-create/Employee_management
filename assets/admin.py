from django.contrib import admin
from .models import Asset, AssetAssignment


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'asset_id',
        'asset_name',
        'asset_type',
        'serial_number',
        'status',
        'purchase_date',
    )

    list_filter = ('asset_type', 'status')
    search_fields = ('asset_id', 'asset_name', 'serial_number')


@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'assignment_id',
        'asset',
        'employee',
        'assigned_date',
        'returned_date',
        'is_returned',
    )

    list_filter = ('is_returned', 'condition_on_assignment')
    search_fields = ('assignment_id', 'employee__first_name', 'asset__asset_name')
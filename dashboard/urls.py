from django.urls import path
from .views import DashboardView, dashboard_page

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('ui/', dashboard_page, name='dashboard_page'),
]
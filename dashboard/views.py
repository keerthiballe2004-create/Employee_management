from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render

from employees.models import Employee
from onboarding.models import OnboardingCase
from offboarding.models import OffboardingCase
from tasks.models import Task
from assets.models import Asset, AssetAssignment
from access_management.models import Access


class DashboardView(APIView):

    def get(self, request):

        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(
            status="COMPLETED"
        ).count()

        data = {
            "employees": {
                "total": Employee.objects.count(),
                "active": Employee.objects.filter(
                    employment_status="ACTIVE"
                ).count(),
                "terminated": Employee.objects.filter(
                    employment_status="TERMINATED"
                ).count(),
                "on_leave": Employee.objects.filter(
                    employment_status="ON_LEAVE"
                ).count(),
                "by_department": list(
                  Employee.objects.values(
                "department__department_name"
                ).annotate(
                 total=Count("employee_id")
                )
            ) ,
            },
           "onboarding": {
           "total": OnboardingCase.objects.count(),
            "not_started": OnboardingCase.objects.filter(
                status="NOT_STARTED"
            ).count(),
            "in_progress": OnboardingCase.objects.filter(
             status="IN_PROGRESS"
            ).count(),
           "completed": OnboardingCase.objects.filter(
              status="COMPLETED"
            ).count(),
            },
           "offboarding": {
           "total": OffboardingCase.objects.count(),
            "requested": OffboardingCase.objects.filter(
              status="REQUESTED"
            ).count(),
            "in_progress": OffboardingCase.objects.filter(
              status="IN_PROGRESS"
            ).count(),
           "completed": OffboardingCase.objects.filter(
              status="COMPLETED"
            ).count(),
            },

        "tasks": {
        "total": total_tasks,
        "completed": completed_tasks,

         "pending": Task.objects.filter(
            status="PENDING"
        ).count(),
        "in_progress":Task.objects.filter(
            status="IN_PROGRESS"
        ).count(),

        "blocked": Task.objects.filter(
           status="BLOCKED"
        ).count(),
        "overdue": Task.objects.filter(
            due_date__lt=timezone.localdate()
        ).exclude(
          status="COMPLETED"
        ).count(),

       "high_priority": Task.objects.filter(
          priority="HIGH"
        ).count(),

       "medium_priority": Task.objects.filter(
          priority="MEDIUM"
        ).count(),

       "low_priority": Task.objects.filter(
          priority="LOW"
        ).count(),
        "by_department":list(
            Task.objects.values(
                "department"
            ).annotate(
                total=Count("task_id")
            )
        ),

        "completion_percentage": round(
            (completed_tasks / total_tasks) * 100, 2
        ) if total_tasks > 0 else 0,
    },
           "assets": {
            "total": Asset.objects.count(),
            "available": Asset.objects.filter(
             status="AVAILABLE"
            ).count(),
           "assigned": Asset.objects.filter(
              status="ASSIGNED"
            ).count(),
            "active_assignments": AssetAssignment.objects.filter(
               is_returned=False
            ).count(),
            "returned_assignments": AssetAssignment.objects.filter(
               is_returned=True
            ).count(),
            "under_maintenance": Asset.objects.filter(
               status="UNDER_MAINTENANCE"
            ).count(),
            },

          "access": {
    "total": Access.objects.count(),

    "pending_approval": Access.objects.filter(
        status="REQUESTED"
    ).count(),

    "approved": Access.objects.filter(
        status="APPROVED"
    ).count(),

    "active": Access.objects.filter(
        status="ACTIVE"
    ).count(),

    "revoked": Access.objects.filter(
        status="REVOKED"
    ).count(),
},
        }

        return Response(data)
def dashboard_page(request):
    return render(request, 'dashboard.html')
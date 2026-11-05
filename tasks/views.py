
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db.models import Count, Q
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.select_related('employee').all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = [
        'department',
        'status',
        'priority',
        'employee'
    ]

    search_fields = [
        'task_id',
        'task_name',
        'assigned_to',
        'employee__first_name',
        'employee__last_name'
    ]

    ordering_fields = [
        'due_date',
        'created_at',
        'priority'
    ]

    @action(detail=False, methods=['get'], url_path='progress')
    def progress(self, request):

        employee_id = request.query_params.get('employee')

        if not employee_id:
            return Response(
                {"error": "Please provide an employee ID."},
                status=400
            )

        task_progress = Task.objects.filter(
            employee_id=employee_id
        ).aggregate(
            total_tasks=Count('task_id'),
            completed_tasks=Count(
                'task_id',
                filter=Q(status='COMPLETED')
            ),
            pending_tasks=Count(
                'task_id',
                filter=Q(status='PENDING')
            ),
            in_progress_tasks=Count(
                'task_id',
                filter=Q(status='IN_PROGRESS')
            ),
            blocked_tasks=Count(
                'task_id',
                filter=Q(status='BLOCKED')
            )
        )

        total = task_progress['total_tasks']
        completed = task_progress['completed_tasks']

        percentage = (
            round((completed / total) * 100, 2)
            if total > 0 else 0
        )

        task_progress['progress_percentage'] = percentage

        return Response(task_progress)


@ensure_csrf_cookie
def tasks_page(request):
    return render(request, 'tasks.html')

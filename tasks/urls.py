from django.urls import path
from .views import (
    KanbanBoardView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateStatusView,
    TaskCommentCreateView,
    TaskAttachmentCreateView,
    TaskUpdateView,
    TaskDeleteView, # Add this import
)

urlpatterns = [
    path('', KanbanBoardView.as_view(), name='kanban_board'), # Kanban board at app root
    path('task/new/', TaskCreateView.as_view(), name='task_new'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'), # Add this pattern
    path('task/<int:pk>/update_status/', TaskUpdateStatusView.as_view(), name='task_update_status'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'), # Add this pattern
    # URLs for adding comments/attachments need the task's pk
    path('task/<int:task_pk>/add_comment/', TaskCommentCreateView.as_view(), name='task_add_comment'),
    path('task/<int:task_pk>/add_attachment/', TaskAttachmentCreateView.as_view(), name='task_add_attachment'),
]
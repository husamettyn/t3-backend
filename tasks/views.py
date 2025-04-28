from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, View # Add DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin # Add this import

from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
import json # For parsing request body in status update

from .models import Task, TaskComment, TaskAttachment
from .forms import TaskForm, TaskCommentForm, TaskAttachmentForm # Need to create these forms

# Kanban Board View
class KanbanBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/kanban_board.html' # Template to be created later

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch tasks and group them by status
        context['todo_tasks'] = Task.objects.filter(status=Task.Status.TODO).order_by('created_at')
        context['inprogress_tasks'] = Task.objects.filter(status=Task.Status.INPROGRESS).order_by('created_at')
        context['done_tasks'] = Task.objects.filter(status=Task.Status.DONE).order_by('created_at')
        context['task_statuses'] = Task.Status.choices # Pass statuses for potential frontend use
        return context

# Task Detail View
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html' # Template to be created later
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = TaskCommentForm() # Add form for creating comments
        context['attachment_form'] = TaskAttachmentForm() # Add form for uploading attachments
        # Potentially add comments and attachments lists here too
        context['comments'] = self.object.comments.order_by('-created_at')
        context['attachments'] = self.object.attachments.order_by('-uploaded_at')
        return context


# Create a new task
class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView): # Add UserPassesTestMixin
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html' # Template to be created later
    success_url = reverse_lazy('kanban_board') # Redirect to board after creation

    # Add test_func to ensure only admins can create tasks
    def test_func(self):
        return self.request.user.is_admin

    # Add get_form to handle admin-only assignment
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only admins can assign tasks to others
        if not self.request.user.is_admin:
            if 'assigned_to' in form.fields:
                # Option 1: Remove the field entirely
                # del form.fields['assigned_to']
                # Option 2: Disable the field
                form.fields['assigned_to'].disabled = True
                form.fields['assigned_to'].required = False
                form.fields['assigned_to'].help_text = "Only admins can assign tasks."
                # Option 3: Hide the field (might need template adjustments)
                # form.fields['assigned_to'].widget = forms.HiddenInput()
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user # Set creator automatically
        # If user is not admin and field was disabled/hidden, ensure assigned_to is not set or is set to None/creator
        if not self.request.user.is_admin:
             form.instance.assigned_to = None # Or self.request.user if self-assignment is desired
        return super().form_valid(form)


# Edit an existing task
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html' # Reuse the create form template

    def get_success_url(self):
        # Redirect back to the detail view of the task being edited
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        # Only creator or admin can edit task details
        task = self.get_object()
        return self.request.user == task.created_by or self.request.user.is_admin

    # Optional: Override get_form similar to TaskCreateView if admin-only assignment logic
    # needs to apply during edit as well (e.g., prevent non-admin from changing assignee).
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only admins can change the assignment
        if not self.request.user.is_admin:
            if 'assigned_to' in form.fields:
                form.fields['assigned_to'].disabled = True
                form.fields['assigned_to'].help_text = "Only admins can change the assignment."
        return form # Ensure return form is correctly indented within get_form


# Delete a task
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html' # Template to be created
    success_url = reverse_lazy('kanban_board') # Redirect to board after deletion

    def test_func(self):
        # Only creator or admin can delete task
        task = self.get_object()
        return self.request.user == task.created_by or self.request.user.is_admin

# Removed orphaned 'return form' from here


# Update Task Status (e.g., via drag-and-drop on frontend)
class TaskUpdateStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        # Task 3.3: Only assigned user or admin can change status
        if not (request.user == task.assigned_to or request.user.is_admin):
             return JsonResponse({'status': 'error', 'message': 'Permission denied. Only the assignee or an admin can change the status.'}, status=403)

        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            if new_status not in Task.Status.values:
                return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)

            task.status = new_status
            task.save()
            return JsonResponse({'status': 'success', 'message': 'Task status updated'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Log the exception e
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred'}, status=500)


# Add a comment to a task
class TaskCommentCreateView(LoginRequiredMixin, CreateView):
    model = TaskComment
    form_class = TaskCommentForm
    template_name = 'tasks/partials/comment_form.html' # Partial template for HTMX/Ajax potentially

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['task_pk'])
        form.instance.task = task
        form.instance.user = self.request.user
        # Handle tagged_users if implemented in form
        super().form_valid(form)
        # Redirect back to the task detail page
        return redirect('task_detail', pk=task.pk)

    def get_success_url(self):
        # This might not be strictly needed if form_valid redirects, but good practice
        return reverse('task_detail', kwargs={'pk': self.kwargs['task_pk']})


# Add an attachment to a task
class TaskAttachmentCreateView(LoginRequiredMixin, CreateView):
    model = TaskAttachment
    form_class = TaskAttachmentForm
    template_name = 'tasks/partials/attachment_form.html' # Partial template

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['task_pk'])
        form.instance.task = task
        form.instance.uploaded_by = self.request.user
        super().form_valid(form)
        return redirect('task_detail', pk=task.pk)

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.kwargs['task_pk']})

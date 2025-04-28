from django import forms
from .models import Task, TaskComment, TaskAttachment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status'] # created_by is set in view
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}), # Smaller text area
        }
        # Add help text or labels if needed
        labels = {
            'assigned_to': 'Assign To',
        }

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['text', 'tagged_users'] # task and user are set in view
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
            'tagged_users': forms.SelectMultiple(attrs={'class': 'select select-multiple'}), # Example for styling
        }
        labels = {
            'text': '', # Hide label for text area
            'tagged_users': 'Tag Users',
        }

class TaskAttachmentForm(forms.ModelForm):
    class Meta:
        model = TaskAttachment
        fields = ['file'] # task and uploaded_by are set in view
        widgets = {
            'file': forms.ClearableFileInput(), # Removed multiple: True
        }
        labels = {
            'file': 'Attach File(s)',
        }
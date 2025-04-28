from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _ # For choices

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', _('To Do')
        INPROGRESS = 'INPROGRESS', _('In Progress')
        DONE = 'DONE', _('Done')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Keep task even if user is deleted, just unassign
        related_name='assigned_tasks',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Delete task if creator is deleted
        related_name='created_tasks'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.TODO,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']


class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/') # Requires Pillow for ImageField validation, FileField is safer if not strictly images
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        # Return filename
        return self.file.name.split('/')[-1]


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    tagged_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tagged_in_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.task.title}"

    class Meta:
        ordering = ['created_at']

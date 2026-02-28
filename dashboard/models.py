from django.db import models
from users.models import User

class ActivityLog(models.Model):
    LEVEL_CHOICES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='info')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Always show newest logs first

    def __str__(self):
        return f"[{self.get_level_display()}] {self.action} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyUser(AbstractUser):
    pass


class Tickets(models.Model):
    title = models.CharField(max_length=50)
    time = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    filed_by = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='filed_by'
    )
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
        ('INVALID', 'Invalid')
    ]
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20,
        default='NEW'
    )
    assigned_to = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='assigned_to',
        blank=True,
        null=True
    )
    completed_by = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='completed_by',
        blank=True,
        null=True
    )
    REQUIRED_FIELDS = ['title', 'description', 'filed_by']

    def __str__(self):
        return self.title

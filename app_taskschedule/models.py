from django.db import models
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.translation import gettext_lazy as _

class TaskSchedule(models.Model):
    TASK_CHOICES = (
        ('app_certifications.tasks.send_weekly_email', 'Schedule Email Certifications'),
        ('app_regulation.tasks.send_weekly_email', 'Schedule Email Regulations'),
        # เพิ่ม task อื่นๆ ที่คุณต้องการ
    )

    task_name = models.CharField(max_length=255, choices=TASK_CHOICES, unique=True)
    day_of_week = models.CharField(max_length=9, blank=True, null=True, help_text=_("Optional. Day of the week as a crontab format, e.g., 'monday', 'tuesday', or '*' for every day."))
    day_of_month = models.CharField(max_length=2, blank=True, null=True, help_text=_("Optional. Day of the month, e.g., '1', '15', or '*' for every day."))
    month_of_year = models.CharField(max_length=5, blank=True, null=True, help_text=_("Optional. Month as a crontab format, e.g., '1' for January, or '*' for every month."))
    hour = models.PositiveIntegerField(help_text=_("Hour in 24-hour format"))
    minute = models.PositiveIntegerField(help_text=_("Minute"))

    send_by_name = models.CharField(default="Siripannee Nonesrivow" ,max_length=255, help_text=_("Name of the email sender"))
    send_by_email = models.EmailField(default="siripannee.n@mcp.meap.com" ,help_text=_("Email of the sender"))

    def __str__(self):
        return self.task_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Update the CrontabSchedule and PeriodicTask
        schedule, created = CrontabSchedule.objects.get_or_create(
            month_of_year=self.month_of_year if self.month_of_year else '*',  # Default to every month if not provided
            day_of_week=self.day_of_week if self.day_of_week else '*',        # Default to every day if not provided
            day_of_month=self.day_of_month if self.day_of_month else '*',     # Default to every day if not provided
            hour=self.hour,
            minute=self.minute
        )

        task, created = PeriodicTask.objects.get_or_create(
            name=self.task_name,
            task=self.task_name,
            defaults={'crontab': schedule}
        )

        # Update the crontab schedule for an existing task
        if not created:
            task.crontab = schedule
            task.save()

        
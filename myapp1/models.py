from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True ,unique=True)
    password = models.CharField(max_length=20)
    profile= models.ImageField(upload_to="photos/",default="default.jpg")
    def __str__(self):
        return self.username
    class Meta:
        db_table = "user"
        verbose_name_plural = "The_Users"

class Incident(models.Model):
    c=[
        ('minor','minor'),
        ('medium', 'medium'),
        ('high', 'high'),
        ('critical', 'critical'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    severity = models.CharField(choices=c)
    file=models.FileField(upload_to="incidents/",default="default.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'incident'
        verbose_name_plural = "Incidents"

class IncidentReport(models.Model):
    incident = models.OneToOneField(
        Incident,
        on_delete=models.CASCADE,
        related_name="report"
    )

    admin_notes = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("reviewed", "Reviewed"),
            ("resolved", "Resolved"),
        ],
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report for: {self.incident.title}"

    class Meta:
        db_table = "incident_report"
        verbose_name_plural = "Incident Reports"



class IncidentHistory(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('edited', 'Edited'),
        ('deleted', 'Deleted'),
    ]

    incident = models.ForeignKey(Incident, on_delete=models.SET_NULL, null=True, related_name="history")
    incident_title = models.CharField(max_length=100, blank=True)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_name = self.performed_by.username if self.performed_by else 'Unknown'
        title = self.incident.title if self.incident else self.incident_title
        return f"{title} - {self.get_action_type_display()} by {user_name}"






# Create your models here.

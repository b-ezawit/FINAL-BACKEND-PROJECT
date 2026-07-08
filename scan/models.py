from django.db import models
import uuid

class ExtractionJob(models.Model):
    # Status choices matching the documentation workflow
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('FAILED', 'Failed'),
    ]

    # Automatically generate a unique UUID string for each job
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    record_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # To store results matching the pre-seeded mock format or real data JSON
    extracted_data = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Job {self.job_id} - {self.status}"
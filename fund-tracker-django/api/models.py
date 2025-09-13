from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        RECEIVER = "RECEIVER", "Receiver"
        STAKEHOLDER = "STAKEHOLDER", "Stakeholder"

    role = models.CharField(max_length=50, choices=Role.choices)

class FundSource(models.Model):
    source_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_name} - ${self.total_amount}"

class Allocation(models.Model):
    fund_source = models.ForeignKey(FundSource, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    registered_location_lon = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

class Proof(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VERIFIED = "VERIFIED", "Verified"
        FLAGGED = "FLAGGED", "Flagged"

    allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to='proofs/')
    file_hash = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField()
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    upload_location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    upload_location_lon = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Proof for {self.allocation.project_name} - {self.status}"
    

class Feedback(models.Model):
    allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback by {self.user.username} on {self.allocation.project_name}'
    

class Feedback(models.Model):
    allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    # ADD THIS NEW LINE for the optional image upload
    image = models.ImageField(upload_to='feedback_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback by {self.user.username} on {self.allocation.project_name}'

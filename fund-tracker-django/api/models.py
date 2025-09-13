from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

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
    # Storing location as two separate fields for simplicity
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
    file_url = models.URLField(max_length=500) # URL from cloud storage like S3/Cloudinary
    file_hash = models.CharField(max_length=64) # SHA-256 hash
    description = models.TextField()
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    upload_location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    upload_location_lon = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    blockchain_tx_hash = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Proof for {self.allocation.project_name} - {self.status}"

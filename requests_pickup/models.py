from django.conf import settings
from django.db import models
from donations.models import FoodDonation


class DonationRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        COMPLETED = 'completed', 'Completed'

    donation = models.ForeignKey(FoodDonation, on_delete=models.CASCADE, related_name='requests')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donation_requests')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    pickup_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requested_by.username} -> {self.donation.food_name} ({self.status})"
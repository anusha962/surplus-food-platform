from django.conf import settings
from django.db import models


class FoodCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)  # veg, non-veg, packaged, cooked

    def __str__(self):
        return self.name


class FoodDonation(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        REQUESTED = 'requested', 'Requested'
        PICKED_UP = 'picked_up', 'Picked Up'
        EXPIRED = 'expired', 'Expired'

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations')
    food_name = models.CharField(max_length=255)
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20, default='kg')  # kg, plates, packets, litres...
    image = models.ImageField(upload_to='donations/', blank=True, null=True)
    prepared_at = models.DateTimeField(null=True, blank=True)
    expiry_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} ({self.status})"
class AIVerificationLog(models.Model):
    donation = models.OneToOneField(FoodDonation, on_delete=models.CASCADE, related_name='ai_verification')
    is_food = models.BooleanField()
    confidence_score = models.FloatField()
    top_label = models.CharField(max_length=100)
    flagged_for_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donation.food_name}: {'OK' if self.is_food else 'FLAGGED'}"
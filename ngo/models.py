from django.conf import settings
from django.db import models


class NGOProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ngo_profile')
    org_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    service_area_radius_km = models.PositiveIntegerField(default=10)
    verified_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Verified" if self.verified_by_admin else "Pending"
        return f"{self.org_name} ({status})"


class Volunteer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='volunteer_profile')
    ngo = models.ForeignKey(NGOProfile, on_delete=models.CASCADE, related_name='volunteers')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} @ {self.ngo.org_name}"
from django.db.models.signals import post_save
from django.dispatch import receiver
from donations.models import FoodDonation
from requests_pickup.models import DonationRequest
from .models import Notification


@receiver(post_save, sender=FoodDonation)
def notify_new_donation(sender, instance, created, **kwargs):
    if not created:
        return
    # Notify every NGO user that a new donation is available.
    from accounts.models import CustomUser
    ngo_users = CustomUser.objects.filter(role=CustomUser.Role.NGO)
    Notification.objects.bulk_create([
        Notification(
            user=ngo,
            message=f"New donation available: {instance.food_name}",
            type=Notification.Type.NEW_DONATION,
        ) for ngo in ngo_users
    ])


@receiver(post_save, sender=DonationRequest)
def notify_request_update(sender, instance, created, **kwargs):
    if created:
        # Notify the donor that someone requested their donation.
        Notification.objects.create(
            user=instance.donation.donor,
            message=f"{instance.requested_by.username} requested your donation: {instance.donation.food_name}",
            type=Notification.Type.REQUEST_UPDATE,
        )
    else:
        # Notify the requester when status changes (accepted/rejected/completed).
        Notification.objects.create(
            user=instance.requested_by,
            message=f"Your request for {instance.donation.food_name} is now {instance.status}",
            type=Notification.Type.REQUEST_UPDATE,
        )
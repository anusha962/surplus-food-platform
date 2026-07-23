from django.core.management.base import BaseCommand
from django.utils import timezone
from donations.models import FoodDonation


class Command(BaseCommand):
    help = "Marks any donation past its expiry_time as expired."

    def handle(self, *args, **options):
        now = timezone.now()
        expired_qs = FoodDonation.objects.filter(
            expiry_time__lt=now,
            status__in=[FoodDonation.Status.AVAILABLE, FoodDonation.Status.REQUESTED],
        )

        count = expired_qs.count()
        expired_qs.update(status=FoodDonation.Status.EXPIRED)

        self.stdout.write(self.style.SUCCESS(f"Marked {count} donation(s) as expired."))
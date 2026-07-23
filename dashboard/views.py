from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.permissions import IsAdminRole
from donations.models import FoodDonation
from ngo.models import NGOProfile
from requests_pickup.models import DonationRequest


class AnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get(self, request):
        total_donations = FoodDonation.objects.count()
        expired_count = FoodDonation.objects.filter(status=FoodDonation.Status.EXPIRED).count()
        picked_up_count = FoodDonation.objects.filter(status=FoodDonation.Status.PICKED_UP).count()
        active_ngos = NGOProfile.objects.filter(verified_by_admin=True).count()
        pending_ngos = NGOProfile.objects.filter(verified_by_admin=False).count()
        completed_requests = DonationRequest.objects.filter(status=DonationRequest.Status.COMPLETED).count()

        expiry_wastage_rate = round((expired_count / total_donations) * 100, 1) if total_donations else 0

        return Response({
            "total_donations": total_donations,
            "meals_saved": picked_up_count,        # donations that actually got picked up
            "completed_requests": completed_requests,
            "active_ngos": active_ngos,
            "pending_ngos": pending_ngos,
            "expired_donations": expired_count,
            "expiry_wastage_rate_percent": expiry_wastage_rate,
            "status_breakdown": {
                "available": FoodDonation.objects.filter(status=FoodDonation.Status.AVAILABLE).count(),
                "requested": FoodDonation.objects.filter(status=FoodDonation.Status.REQUESTED).count(),
                "picked_up": picked_up_count,
                "expired": expired_count,
            }
        })
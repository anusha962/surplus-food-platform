from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.permissions import IsNGO
from donations.models import FoodDonation
from .models import DonationRequest
from .serializers import DonationRequestSerializer


class DonationRequestViewSet(viewsets.ModelViewSet):
    serializer_class = DonationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # NGOs see their own requests; donors see requests on their donations
        if user.role == 'ngo':
            return DonationRequest.objects.filter(requested_by=user)
        elif user.role == 'donor':
            return DonationRequest.objects.filter(donation__donor=user)
        return DonationRequest.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsNGO()]
        return super().get_permissions()

    def perform_create(self, serializer):
        donation = serializer.validated_data['donation']
        if donation.status != FoodDonation.Status.AVAILABLE:
            raise serializers.ValidationError("This donation is no longer available.")
        serializer.save(requested_by=self.request.user)
        donation.status = FoodDonation.Status.REQUESTED
        donation.save()

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        req = self.get_object()
        if req.donation.donor != request.user:
            return Response({"detail": "Only the donor can accept this."}, status=status.HTTP_403_FORBIDDEN)
        req.status = DonationRequest.Status.ACCEPTED
        req.save()
        return Response(DonationRequestSerializer(req).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        req = self.get_object()
        if req.donation.donor != request.user:
            return Response({"detail": "Only the donor can reject this."}, status=status.HTTP_403_FORBIDDEN)
        req.status = DonationRequest.Status.REJECTED
        req.donation.status = FoodDonation.Status.AVAILABLE
        req.donation.save()
        req.save()
        return Response(DonationRequestSerializer(req).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        req = self.get_object()
        if req.donation.donor != request.user:
            return Response({"detail": "Only the donor can mark this complete."}, status=status.HTTP_403_FORBIDDEN)
        req.status = DonationRequest.Status.COMPLETED
        req.donation.status = FoodDonation.Status.PICKED_UP
        req.donation.save()
        req.save()
        return Response(DonationRequestSerializer(req).data)
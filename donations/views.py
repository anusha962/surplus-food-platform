from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.permissions import IsOwnerOrReadOnly
from .models import FoodDonation, FoodCategory, AIVerificationLog
from .serializers import FoodDonationSerializer, FoodCategorySerializer
from .utils import haversine_km
from .ai_client import verify_food_image


class FoodCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class FoodDonationViewSet(viewsets.ModelViewSet):
    serializer_class = FoodDonationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    owner_field = 'donor'

    def get_queryset(self):
        return FoodDonation.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        donation = serializer.save(donor=self.request.user)

        if donation.image:
            result = verify_food_image(donation.image)
            if result:
                top = result["top_predictions"][0]
                AIVerificationLog.objects.create(
                    donation=donation,
                    is_food=result["is_food"],
                    confidence_score=top["confidence"],
                    top_label=top["label"],
                    flagged_for_review=not result["is_food"],
                )

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius_km = float(request.query_params.get('radius_km', 10))

        if not lat or not lng:
            return Response({"detail": "lat and lng query params are required."}, status=400)

        results = []
        for donation in FoodDonation.objects.filter(status='available'):
            if donation.latitude is None or donation.longitude is None:
                continue
            distance = haversine_km(lat, lng, donation.latitude, donation.longitude)
            if distance <= radius_km:
                data = FoodDonationSerializer(donation).data
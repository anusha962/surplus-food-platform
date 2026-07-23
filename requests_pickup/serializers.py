from rest_framework import serializers
from .models import DonationRequest


class DonationRequestSerializer(serializers.ModelSerializer):
    requested_by_username = serializers.ReadOnlyField(source='requested_by.username')
    donation_name = serializers.ReadOnlyField(source='donation.food_name')
    donor_username = serializers.ReadOnlyField(source='donation.donor.username')

    class Meta:
        model = DonationRequest
        fields = (
            'id', 'donation', 'donation_name', 'donor_username',
            'requested_by', 'requested_by_username',
            'status', 'pickup_time', 'created_at',
        )
        read_only_fields = ('id', 'requested_by', 'status', 'created_at')
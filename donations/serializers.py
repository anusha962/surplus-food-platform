from rest_framework import serializers
from .models import FoodDonation, FoodCategory


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id', 'name')


class FoodDonationSerializer(serializers.ModelSerializer):
    donor = serializers.ReadOnlyField(source='donor.username')

    class Meta:
        model = FoodDonation
        fields = (
            'id', 'donor', 'food_name', 'category', 'quantity', 'unit',
            'image', 'prepared_at', 'expiry_time', 'status',
            'latitude', 'longitude', 'created_at',
        )
        read_only_fields = ('id', 'donor', 'status', 'created_at')
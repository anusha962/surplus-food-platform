from rest_framework import serializers
from .models import NGOProfile, Volunteer


class NGOProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = NGOProfile
        fields = (
            'id', 'username', 'org_name', 'registration_number',
            'service_area_radius_km', 'verified_by_admin', 'created_at',
        )
        read_only_fields = ('id', 'verified_by_admin', 'created_at')


class VolunteerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    ngo_name = serializers.ReadOnlyField(source='ngo.org_name')

    class Meta:
        model = Volunteer
        fields = ('id', 'username', 'ngo', 'ngo_name', 'joined_at')
        read_only_fields = ('id', 'joined_at')
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from accounts.permissions import IsNGO
from .models import NGOProfile
from .serializers import NGOProfileSerializer


class MyNGOProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = NGOProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsNGO]

    def get_object(self):
        try:
            return self.request.user.ngo_profile
        except NGOProfile.DoesNotExist:
            raise NotFound("You haven't created an NGO profile yet.")


class NGOProfileCreateView(generics.CreateAPIView):
    serializer_class = NGOProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsNGO]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
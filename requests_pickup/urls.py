from rest_framework.routers import DefaultRouter
from .views import DonationRequestViewSet

router = DefaultRouter()
router.register('requests', DonationRequestViewSet, basename='donation-request')

urlpatterns = router.urls
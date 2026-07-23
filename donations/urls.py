from rest_framework.routers import DefaultRouter
from .views import FoodDonationViewSet, FoodCategoryViewSet

router = DefaultRouter()
router.register('donations', FoodDonationViewSet, basename='donation')
router.register('categories', FoodCategoryViewSet, basename='category')

urlpatterns = router.urls
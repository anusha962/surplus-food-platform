from django.contrib import admin
from .models import FoodDonation, FoodCategory, AIVerificationLog


admin.site.register(FoodCategory)
admin.site.register(FoodDonation)


@admin.register(AIVerificationLog)
class AIVerificationLogAdmin(admin.ModelAdmin):
    list_display = ('donation', 'is_food', 'confidence_score', 'top_label', 'flagged_for_review', 'created_at')
    list_filter = ('flagged_for_review', 'is_food')
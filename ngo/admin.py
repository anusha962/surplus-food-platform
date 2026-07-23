from django.contrib import admin
from .models import NGOProfile, Volunteer


@admin.register(NGOProfile)
class NGOProfileAdmin(admin.ModelAdmin):
    list_display = ('org_name', 'user', 'registration_number', 'verified_by_admin', 'created_at')
    list_filter = ('verified_by_admin',)
    actions = ['verify_ngos']

    def verify_ngos(self, request, queryset):
        queryset.update(verified_by_admin=True)
    verify_ngos.short_description = "Mark selected NGOs as verified"


admin.site.register(Volunteer)
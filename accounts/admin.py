from django.contrib import admin
from .models import User,UserPickupLocation
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email','full_name', 'profile_picture','role', 'subscription_plan','contact_number', 'is_active','is_staff','is_superuser')
    # readonly_fields = ('otp',)
    
admin.site.register(User,CustomUserAdmin)
# Register your models here.
admin.site.register(UserPickupLocation)
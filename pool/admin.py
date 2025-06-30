from django.contrib import admin
from .models import Pool, PoolMember

class PoolMemberInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = PoolMember
    extra = 0  # Number of empty forms to display for adding new PoolMembers
    fields = ('user', 'role', 'status', 'pickup_location_lat', 'pickup_location_lng','driving_days', 'joined_at')
    readonly_fields = ('joined_at',)

@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'departure_location', 'arrival_location', 'start_date', 'start_time', 'is_return_trip')
    inlines = [PoolMemberInline]


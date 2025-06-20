from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from vehicle.models import Vehicle
from children.models import Children

# Create your models here.
# Pool Model
class Pool(models.Model):
    REPEAT_CHOICES = [
        ('DoNotRepeat', _('Do not repeat')),
        ('Daily', _('Daily')),
        ('Weekly', _('Weekly')),
        ('Custom', _('Custom')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pools_created')
    name = models.CharField(_('pool name'), max_length=255)
    departure_location = models.CharField(_('departure location'), max_length=255)
    arrival_location = models.CharField(_('arrival location'), max_length=255, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name='pools', blank=True, null=True)
    repeat_type = models.CharField(_('repeat type'), max_length=20, choices=REPEAT_CHOICES, default='DoNotRepeat')
    scheduled_days = models.CharField(_('scheduled days'), max_length=255,blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    is_return_trip = models.BooleanField(_('return trip'), default=False)
    return_time = models.TimeField(_('return time'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.name
    



# PoolMember Model
class PoolMember(models.Model):
    ROLE_CHOICES = [
        ('Member', _('Member')),
        ('Driver', _('Driver')),
        ('Admin', _('Admin')),
    ]
    STATUS_CHOICES = [
        ('Pending', _('Pending')),
        ('Approved', _('Approved')),
        ('Rejected', _('Rejected')),
        ('Leave', _('Leave')),
    ]

    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pool_memberships')
    children = models.ManyToManyField(Children, blank=True, related_name='pool_members')
    role = models.CharField(_('role'), max_length=10, choices=ROLE_CHOICES, default='Member')
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='Pending')
    driving_days = models.CharField(_('driving days'), max_length=255, blank=True, null=True)
    joined_at = models.DateTimeField(_('joined at'), auto_now_add=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        unique_together = ('pool', 'user')

    def __str__(self):
        return f"{self.user.full_name} - {self.pool.name}"
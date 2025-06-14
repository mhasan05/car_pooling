from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Parent', 'Parent'),
        ('Admin', 'Admin'),
        ('Driver', 'Driver'),
    ]
    SUBSCRIPTION_PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Parent')
    subscription_plan = models.CharField(max_length=10, choices=SUBSCRIPTION_PLAN_CHOICES, default='Basic')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

# Vehicle Model
class Vehicle(models.Model):
    VEHICLE_TYPE = [
        ('Car', 'Car'),
        ('SUV', 'SUV'),
        ('Truck', 'Truck'),
        ('Van', 'Van'),
    ]
    COLOR = [
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Black', 'Black'),
        ('White', 'White'),
        ('Yellow', 'Yellow'),
        ('Brown', 'Brown'),
        ('Orange', 'Orange'),
        ('Purple', 'Purple'),
        ('Gold', 'Gold'),
        ('Beige', 'Beige'),
        ('Maroon', 'Maroon'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make_model = models.CharField(max_length=200)
    color = models.CharField(max_length=20, choices=COLOR)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE)
    seats = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=50, unique=True, blank=True, null=True)
    

# Pool Model
class Pool(models.Model):
    pool_name = models.CharField(max_length=255)
    departure_location = models.CharField(max_length=255)
    arrival_location = models.CharField(max_length=255, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='pools', blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    scheduled_days = models.CharField(max_length=255, help_text="Comma-separated days of the week (e.g., Mon,Tue,Wed)")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_pools')
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# PoolMember Model
class PoolMember(models.Model):
    ROLE_CHOICES = [
        ('Member', 'Member'),
        ('Admin', 'Admin'),
    ]

    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pool_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pool', 'user')

# Ride Model
class Ride(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='driven_rides')
    scheduled_datetime = models.DateTimeField()
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    alternate_location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

# RideParticipant Model
class RideParticipant(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_requests')
    kid_name = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)

# Subscription Model
class Subscription(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('Stripe', 'Stripe'),
        ('PayPal', 'PayPal'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Expired', 'Expired'), ('Cancelled', 'Cancelled')], default='Active')

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from accounts.models import Children


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

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Parent', _('Parent')),
        ('Admin', _('Admin')),
        ('Driver', _('Driver')),
    ]
    SUBSCRIPTION_PLAN_CHOICES = [
        ('Basic', _('Basic')),
        ('Premium', _('Premium')),
    ]

    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=255)
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, default='Parent')
    subscription_plan = models.CharField(_('subscription plan'), max_length=10, choices=SUBSCRIPTION_PLAN_CHOICES, default='Basic')
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pictures/', blank=True, null=True)
    contact_number = models.CharField(_('contact number'), max_length=20, blank=True, null=True)
    total_rides = models.PositiveIntegerField(_('total rides'), default=0)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


# Vehicle Model
class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('Car', _('Car')),
        ('SUV', _('SUV')),
        ('Truck', _('Truck')),
        ('Van', _('Van')),
    ]
    COLOR_CHOICES = [
        ('Red', _('Red')), ('Blue', _('Blue')), ('Green', _('Green')),
        ('Black', _('Black')), ('White', _('White')), ('Yellow', _('Yellow')),
        ('Brown', _('Brown')), ('Orange', _('Orange')), ('Purple', _('Purple')),
        ('Gold', _('Gold')), ('Beige', _('Beige')), ('Maroon', _('Maroon')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make_model = models.CharField(_('make and model'), max_length=200)
    color = models.CharField(_('color'), max_length=20, choices=COLOR_CHOICES)
    vehicle_type = models.CharField(_('vehicle type'), max_length=20, choices=VEHICLE_TYPE_CHOICES)
    seats = models.PositiveIntegerField(_('seating capacity'))
    license_plate = models.CharField(_('license plate'), max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.make_model} ({self.license_plate})" 


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
    scheduled_days = models.CharField(
        _('scheduled days'), max_length=255, 
        help_text=_("Comma-separated days of the week (e.g., Mon,Tue,Wed)"), 
        blank=True, null=True
    )
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


# PickupLocation Model
class PickupLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickup_locations')
    title = models.CharField(_('title'), max_length=100, default='Location')
    address = models.CharField(_('address'), max_length=500)

    def __str__(self):
        return self.title


# Subscription Model
class Subscription(models.Model):
    PLAN_CHOICES = [
        ('Basic', _('Basic')),
        ('Premium', _('Premium')),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('Stripe', _('Stripe')),
        ('PayPal', _('PayPal')),
        ('Other', _('Other')),
    ]
    STATUS_CHOICES = [
        ('Active', _('Active')),
        ('Expired', _('Expired')),
        ('Cancelled', _('Cancelled')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan_name = models.CharField(_('plan name'), max_length=20, choices=PLAN_CHOICES)
    payment_method = models.CharField(_('payment method'), max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'), blank=True, null=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.user.email} - {self.plan_name}"

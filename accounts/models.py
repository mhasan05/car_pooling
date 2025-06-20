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
    ]
    SUBSCRIPTION_PLAN_CHOICES = [
        ('Basic', _('Basic')),
        ('Premium', _('Premium')),
    ]

    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=255,null=True,blank=True)
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, default='Parent')
    subscription_plan = models.CharField(_('subscription plan'), max_length=10, choices=SUBSCRIPTION_PLAN_CHOICES, default='Basic')
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pictures/', blank=True, null=True)
    contact_number = models.CharField(_('contact number'), max_length=20, blank=True, null=True)
    total_rides = models.PositiveIntegerField(_('total rides'), default=0)
    otp = models.PositiveIntegerField(_('OTP'), null=True,blank=True)
    is_active = models.BooleanField(_('active status'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    




class UserPickupLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickup_location')
    pickup_location = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pickup_location

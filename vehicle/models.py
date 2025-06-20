from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _

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
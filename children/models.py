from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _

class Children(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    child_name = models.CharField(max_length=100)
    dob = models.DateField()
    image = models.ImageField(upload_to='child/', blank=True, null=True)

    def __str__(self):
        return self.child_name
    
    class Meta:
        verbose_name = _('child')
        verbose_name_plural = _('children')
        ordering = ['child_name']
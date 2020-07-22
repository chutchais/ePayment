from django.db              import models
from django.conf            import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.urls            import reverse
import json

# Create your models here.
class Booking(models.Model):
    TERMINAL_CHOICES = (
            ('LCB1', 'LCB1'),
            ('LCMT', 'LCMT'),
        )

    name                = models.CharField(max_length=100,
                            verbose_name='Booking number',
                            validators=[
                                RegexValidator(
                                    regex='^[\w-]+$',
                                    message='Name does not allow special charecters',
                                ),
                            ])
    terminal            = models.CharField(max_length=10,blank=True,null=True
                            ,choices=TERMINAL_CHOICES)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
    status              = models.BooleanField(default=True)
    user                = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            blank=True,null=True)
    class Meta:
        unique_together = [['name', 'user']]
        indexes = [
            models.Index(fields=['name'],name='idx_booking_booking_name'),
        ]

    def __str__(self):  # __unicode__ for Python 2
        return self.name

    def get_absolute_url(self):
        return reverse('booking:detail', kwargs={'pk': self.pk})

    @property
    def order_count(self):
        qty = self.orders.count()
        return qty
    order_count.fget.short_description = "Total Order"
from django.db              import models
from django.conf 	        import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.urls            import reverse
import json

from booking.models import Booking
from user_profile.models import Address
# Create your models here.
# class Booking(models.Model):
#     name                = models.CharField(max_length=100,
#                             validators=[
#                                 RegexValidator(
#                                     regex='^[\w-]+$',
#                                     message='Name does not allow special charecters',
#                                 ),
#                             ])
#     created             = models.DateTimeField(auto_now_add=True)
#     updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
#     status              = models.BooleanField(default=True)
#     user 			    = models.ForeignKey(settings.AUTH_USER_MODEL,
#                             on_delete=models.SET_NULL,
#                             blank=True,null=True)

#     def __str__(self):  # __unicode__ for Python 2
#         return self.name

def image_file_name(instance, filename):
    return 'images/order/%s/%s/%s' % (instance.booking,instance.ref, filename)

class Order(models.Model):
    name                = models.CharField(max_length=50,
                            validators=[
                                RegexValidator(
                                    regex='^[\w-]+$',
                                    message='Name does not allow special charecters',
                                ),
                            ])
    ref                 = models.CharField(max_length=6) #keep time stamp  'hhmmss'
    booking             = models.ForeignKey(Booking,
                            on_delete=models.CASCADE,
                            blank=True, null=True,
                            related_name = 'orders')
    address             = models.ForeignKey(Address,
                            on_delete=models.SET_NULL,
                            blank=True, null=True,
                            related_name = 'orders')
    container_count     = models.IntegerField(default=0)
    charge              = models.FloatField(default=0)
    vat_rate            = models.IntegerField(default=7)
    wht_rate            = models.IntegerField(default=3)
    wht                 = models.BooleanField(default=False)
    grand_total         = models.FloatField(default=0)
    paid                = models.BooleanField(default=False)
    payment_date        = models.DateTimeField(blank=True, null=True)
    payment_ref         = models.CharField(max_length=50,blank=True, null=True)
    payment_slip        = models.ImageField(upload_to=image_file_name,blank=True, null=True)
    payment_inspector   = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            blank=True,null=True,related_name = 'inspect_orders')
    execute_job         = models.BooleanField(default=False)
    execute_date        = models.DateTimeField(blank=True, null=True)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
    status              = models.BooleanField(default=True)
    user 			    = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            blank=True,null=True,related_name = 'orders')
    qrid                = models.CharField(max_length=30,blank=True, null=True)
    seperate_bill       = models.BooleanField(default=False)#Added on Oct 8,2020
    wht_slip            = models.ImageField(upload_to=image_file_name,blank=True, null=True)#Added on Oct 28,2020
    execute_by          = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            blank=True,null=True,related_name = 'execute_orders')

    def __str__(self):  # __unicode__ for Python 2
        return self.name

    class Meta:
        permissions = [
            ('verify_payment', 'Can verify payment'),
            ('update_payment', 'Can update payment'),
            ('execute_job', 'Can execute job')
        ]
        indexes = [
            models.Index(fields=['name'],name='idx_order_order_name'),
            models.Index(fields=['qrid'],name='idx_order_qrid')
        ]

    def get_absolute_url(self):
        return reverse('order:detail', kwargs={'pk': self.pk})

    # @property
    # def slip_image_url(self):
    #     if self.payment_slip:
    #         return self.payment_slip.url
    #     return '#'

    # @property
    # def container_count(self):
    #     qty = self.containers.count()
    #     return qty
    # container_count.fget.short_description = "Total Container"

    @property
    def vat_total(self):
        total = self.charge * self.vat_rate/100
        return total
    vat_total.fget.short_description = "Vat Total"

    @property
    def wht_total(self):
        qty = self.charge * self.wht_rate/100
        return qty
    vat_total.fget.short_description = "Vat Total"

class Container(models.Model):
    container           = models.CharField(max_length=15)
    order               = models.ForeignKey(Order,
                            on_delete=models.CASCADE,
                            blank=True, null=True,
                            related_name = 'containers')
    cont_size           = models.IntegerField(default=40)
    iso                 = models.CharField(max_length=10,default='22G1')
    is_oog              = models.BooleanField(default=False)
    tariff              = models.TextField(max_length=300,null=True,blank=True)
    total               = models.FloatField(default=0)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
    status              = models.BooleanField(default=True)
    user 			    = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            blank=True,null=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.container

    def get_absolute_url(self):
        return reverse('order:container-detail', kwargs={'pk': self.pk})

    @property
    def tariff_json(self):
        import ast
        # print(self.tariff)
        if self.tariff :
            return ast.literal_eval(self.tariff)
        return {}
    
    class Meta:
        indexes = [
            models.Index(fields=['container'],name='idx_order_container_container'),
        ]

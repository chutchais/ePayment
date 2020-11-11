from django.db              import models
from django.conf            import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.urls            import reverse
import json

# from shorepass.models import Pod,Agent
# Create your models here.

class Agent(models.Model):
    name                = models.CharField(primary_key=True,max_length=10,
                            verbose_name='Line/Agent name',
                            validators=[
                                RegexValidator(
                                    regex='^[\w-]+$',
                                    message='Agent does not allow special charecters',
                                ),
                            ])
    fullname            = models.CharField(max_length=100,blank=True, null=True)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
    status              = models.BooleanField(default=True)
    user                = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            blank=True,null=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):  # __unicode__ for Python 2
        return f'{self.name} : {self.fullname}'

    def get_absolute_url(self):
        return reverse('shorepass:agentdetail', kwargs={'pk': self.pk})


class Pod(models.Model):
    name                = models.CharField(primary_key=True,max_length=20,
                            verbose_name='Port of Discharge',
                            validators=[
                                RegexValidator(
                                    regex='^[\w-]+$',
                                    message='Pod does not allow special charecters',
                                ),
                            ])
    description         = models.CharField(max_length=100,blank=True, null=True)
    actual_pod          = models.CharField(max_length=20,blank=True, null=True)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
    status              = models.BooleanField(default=True)
    user                = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            blank=True,null=True)
    def __str__(self):  # __unicode__ for Python 2
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('shorepass:poddetail', kwargs={'pk': self.pk})
        
def image_file_name(instance, filename):
    return 'images/shore/%s/%s' % (instance.shore.booking, filename)

class Shore(models.Model):
    TERMINAL_CHOICES = (
            ('LCB1', 'LCB1'),
            ('LCMT', 'LCMT'),
        )
    booking             = models.CharField(max_length=100,
                            verbose_name='Booking number',
                            validators=[
                                RegexValidator(
                                    regex='^[\w-]+$',
                                    message='Name does not allow special charecters',
                                ),
                            ])
    terminal            = models.CharField(max_length=10,blank=True,null=True
                            ,choices=TERMINAL_CHOICES)
    vessel_name         = models.CharField(max_length=100)
    pod                 = models.ForeignKey(Pod,
                            on_delete=models.CASCADE,
                            blank=True,null=True,related_name='shores')
    # pod             = models.CharField(max_length=100)
    agent               = models.ForeignKey(Agent,
                            on_delete=models.CASCADE,
                            blank=True,null=True,related_name='shores')
    voy                 = models.CharField(max_length=20,
                            validators=[
                                    RegexValidator(
                                        regex='^[\w-]+$',
                                        message='Voy does not allow special charecters',
                                    ),
                                ])
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
    status              = models.BooleanField(default=True)
    user                = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            blank=True,null=True)
    execute_job         = models.BooleanField(default=False)
    execute_date        = models.DateTimeField(blank=True, null=True)
    execute_by          = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            blank=True,null=True,related_name = 'execute_shore')
    customer_name       = models.CharField(max_length=500,blank=True, null=True)
    
    class Meta:
        # unique_together = [['booking', 'user']]
        permissions = [
            ('verify_shore', 'Can verify shorepass document'),
            ('execute_shore', 'Can execute shore')
        ]
        indexes = [
            models.Index(fields=['user'],name='idx_shorepass_shore_user'),
            models.Index(fields=['booking'],name='idx_shorepass_shore_booking'),
            models.Index(fields=['vessel_name'],name='idx_shorepass_shore_vesselname'),
        ]
    
    def __str__(self):  # __unicode__ for Python 2
        return self.booking

    def get_absolute_url(self):
        return reverse('shorepass:shoredetail', kwargs={'pk': self.pk})

class Container(models.Model):
    pass

class Document(models.Model):
    shore               = models.ForeignKey(Shore,
                            on_delete=models.CASCADE,
                            blank=True, null=True,
                            related_name = 'documents')
    shorefile           = models.ImageField(upload_to=image_file_name,blank=True, null=True)
    title               = models.CharField(max_length=100,blank=True,null=True)
    created             = models.DateTimeField(auto_now_add=True)



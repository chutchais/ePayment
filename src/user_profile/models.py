from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def image_file_name(instance, filename):
    return 'images/profiles/%s/%s' % (instance.user.username, filename)

class Profile(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed     = models.BooleanField(default=False)
    avartar             = models.ImageField(upload_to=image_file_name,blank=True, null=True)
    idcard              = models.ImageField(upload_to=image_file_name,blank=True, null=True)
    signature           = models.ImageField(upload_to=image_file_name,blank=True, null=True)
    lineid              = models.CharField(max_length=100,blank=True, null=True)
    approved 			= models.BooleanField(default=False)
    approved_date		= models.DateTimeField(blank=True, null=True)
    # Added on Oct 22,2020 -- Add Telephone number
    phone               = models.CharField(max_length=100,blank=True, null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Address(models.Model):
    user             = models.ForeignKey(User, null=True,blank = True,
                            on_delete=models.SET_NULL,
                            related_name='addresses')
    company             = models.CharField(max_length=100)
    address             = models.CharField(max_length=300)
    tax                 = models.CharField(max_length=20,null=True,blank = True)
    branch              = models.CharField(max_length=30,null=True,blank = True)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
    status              = models.BooleanField(default=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.company

    @property
    def full_address(self):
        return f"{self.company} {self.address} {self.tax}"
    full_address.fget.short_description = "Full Address"
from django.db import models
from django.conf 	        import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
class Tax(models.Model):
    name                = models.CharField(max_length=100,
                            validators=[
                                RegexValidator(
                                    regex='^[\w-]+$',
                                    message='Name does not allow special charecters',
                                ),
                            ])
    tax                 = models.FloatField(default=7,verbose_name='Tax rate')
    wht                 = models.FloatField(default=3,verbose_name='With Holding Tax')
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
    status              = models.BooleanField(default=True)
    user 			    = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            blank=True,null=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.name

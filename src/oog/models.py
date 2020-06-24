from django.db              import models
from django.conf 	        import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
class Oog(models.Model):
    booking             = models.CharField(max_length=50,
                            validators=[
                                RegexValidator(
                                    regex='^[\w-]+$',
                                    message='Booking does not allow special charecters',
                                ),
                            ])
    container           = models.CharField(max_length=13)
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
    status              = models.BooleanField(default=True)
    user 			    = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL,
                            blank=True,null=True)
    class Meta:
        unique_together = ['booking', 'container']

    def __str__(self):  # __unicode__ for Python 2
        return f'{self.container} on {self.booking}'
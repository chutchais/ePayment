from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.
class ContainerType(models.Model):
	name             	= models.CharField(max_length=10,primary_key=True,
								validators=[
									RegexValidator(
										regex='^[\w-]+$',
										message='Name does not allow special charecters',
									),
								])
	title             	= models.CharField(max_length=100)
	created             = models.DateTimeField(auto_now_add=True)
	updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
	status              = models.BooleanField(default=True)
	user             	= models.ForeignKey(User, null=True,blank = True,
                            on_delete=models.SET_NULL,
                            related_name='containertypes')

	def __str__(self):  # __unicode__ for Python 2
	    return self.name

class ContainerProfile(models.Model):
	CATEGORY_CHOICES = (
	        ('E', 'Export'),
	        ('I', 'Import'),
	        ('B', 'Import and Export'),
	    )
	category 			= models.CharField(max_length=2,choices=CATEGORY_CHOICES,default='B')
	full 				= models.BooleanField(default=True)
	oog					= models.BooleanField(default=False)
	reef				= models.BooleanField(default=False)
	note             	= models.CharField(max_length=100,blank=True, null=True)
	created             = models.DateTimeField(auto_now_add=True)
	updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
	status              = models.BooleanField(default=True)
	user             	= models.ForeignKey(User, null=True,blank = True,
                            on_delete=models.SET_NULL,
                            related_name='containerprofiles')
	class meta:
		unique_together = ['category', 'full','oog','reef']

	def __str__(self):  # __unicode__ for Python 2
	    return f'{self.note}'

class Tariff(models.Model):
	# name             	= models.CharField(max_length=100,primary_key=True,
	# 						validators=[
	# 								RegexValidator(
	# 									regex='^[\w-]+$',
	# 									message='Name does not allow special charecters',
	# 								),
	# 							])
	seq 				= models.IntegerField(default=10)
	container_profile   = models.ForeignKey(ContainerProfile, 
							null=True,blank = True,
	                        on_delete=models.SET_NULL,
	                        related_name='tariff_items')
	title             	= models.CharField(max_length=100,blank=True, null=True)
	note             	= models.CharField(max_length=100,blank=True, null=True)
	size20				= models.FloatField(default=0)
	size40				= models.FloatField(default=0)
	size45				= models.FloatField(default=0)
	created             = models.DateTimeField(auto_now_add=True)
	updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
	status              = models.BooleanField(default=True)
	user             	= models.ForeignKey(User, null=True,blank = True,
                            on_delete=models.SET_NULL,
                            related_name='tariffs')
	class meta:
		ordering = ['container_profile','-seq']

	def __str__(self):  # __unicode__ for Python 2
	    return self.title

# class TariffItem(models.Model):
# 	tariff             	= models.ForeignKey(Tariff, 
# 							null=True,blank = True,
#                             on_delete=models.SET_NULL,
#                             related_name='items')
# 	# container_type      = models.ForeignKey(ContainerType, 
# 	# 						null=True,blank = True,
#  #                            on_delete=models.SET_NULL,
#  #                            related_name='tariff_items')
# 	full 				= models.BooleanField(default=True)
# 	oog					= models.BooleanField(default=False)
# 	size20				= models.FloatField(default=0)
# 	size40				= models.FloatField(default=0)
# 	size45				= models.FloatField(default=0)
# 	note             	= models.CharField(max_length=100,blank=True, null=True)
# 	created             = models.DateTimeField(auto_now_add=True)
# 	updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
# 	status              = models.BooleanField(default=True)
# 	user             	= models.ForeignKey(User, null=True,blank = True,
#                             on_delete=models.SET_NULL,
#                             related_name='tariff_items')

# 	def __str__(self):  # __unicode__ for Python 2
# 	    return f'{self.tariff}'





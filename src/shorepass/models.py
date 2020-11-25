from django.db              import models
from django.conf            import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.urls            import reverse
import json
from django.db.models.signals import post_save,pre_save,pre_delete

# from shorepass.models import Pod,Agent
# Create your models here.

class Agent(models.Model):
	name                = models.CharField(primary_key=True,max_length=100,
							verbose_name='Line/Agent name',
							validators=[
								RegexValidator(
									regex='^[\w-]+$',
									message='Agent does not allow special charecters',
								),
							])
	fullname            = models.CharField(max_length=200,blank=True, null=True)
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
	class Meta:
		ordering =['name']

	def __str__(self):  # __unicode__ for Python 2
		return f'{self.name}'

	def get_absolute_url(self):
		return reverse('shorepass:poddetail', kwargs={'pk': self.pk})
		
def image_file_name(instance, filename):
	return 'images/shore/%s/%s' % (instance.shore.booking, filename)

def image_shore_file_name(instance, filename):
	return 'images/shore/%s/%s' % (instance.booking, filename)

class Customer(models.Model):
	name                = models.CharField(max_length=200,
							verbose_name='Customer name')
	address             = models.CharField(max_length=300,null=True,blank = True)
	tax                 = models.CharField(max_length=20,null=True,blank = True)
	branch              = models.CharField(max_length=30,null=True,blank = True)
	description         = models.CharField(max_length=200,blank=True, null=True)
	created             = models.DateTimeField(auto_now_add=True)
	updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
	status              = models.BooleanField(default=True)
	user                = models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.SET_NULL,
							blank=True,null=True)
	class Meta:
		ordering = ['name']
		unique_together = [['name', 'tax']]
		indexes = [
			models.Index(fields=['name'],name='idx_shorepass_customer_name'),
			models.Index(fields=['tax'],name='idx_shorepass_customer_tax')
		]

	def __str__(self):  # __unicode__ for Python 2
		return f'{self.name}'

	def get_absolute_url(self):
		return reverse('shorepass:customerdetail', kwargs={'pk': self.pk})
		
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
	# Removed on Nov 18,2020 
	# customer_name       = models.CharField(max_length=500,blank=True, null=True)
	customer            = models.ForeignKey(Customer,
							on_delete=models.SET_NULL,
							blank=True,null=True,related_name='shores')
	
	# Added on Nov 24,2020 -- To save attached file.
	shorefile1           = models.ImageField(upload_to=image_shore_file_name,blank=True, null=True)
	shorefile2           = models.ImageField(upload_to=image_shore_file_name,blank=True, null=True)
	# for keep containers in json format
	containers_json      = models.TextField(blank=True, null=True)
	# Added on Nov 25,2020 -- To support Contact staff feature.
	need_contact		= models.BooleanField(default=False)
	message 			= models.TextField(blank=True, null=True)

	
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
	
	@property
	def container_count(self):
		qty = self.containers.count()
		return qty
	container_count.fget.short_description = "Total Container"

def post_save_shore_receiver(sender, instance,created, *args, **kwargs):
	# if not instance.executed :
	if created :
		if instance.containers_json:
			import json
			containers_json = json.loads(instance.containers_json)
			for container in containers_json:
				c = Container(shore=instance,
					number=container['name'],
					cont_size=container['size'],
					cont_type=container['container_type'],
					temperature = 0 if container['temperature'] == '' else container['temperature'],
					stowage=container['stowage'],
					user=instance.user)
				c.save()
				print(f'Container : {c} --Successful')

		# instance.save()
		# print (f'Saved data of {instance.goodcode} -- {instance.invecode}')

post_save.connect(post_save_shore_receiver, sender=Shore)
# class Container(models.Model):
#     pass

class Container(models.Model):
	STOWAGE_CHOICES = (
			('UD', 'Underdeck'),
			('OD', 'Overdeck'),
		)
	number           = models.CharField(max_length=15,blank=True,null=True)
	shore               = models.ForeignKey(Shore,
							on_delete=models.CASCADE,
							blank=True, null=True,
							related_name = 'containers')
	cont_size           = models.IntegerField(default=40)
	cont_type           = models.CharField(max_length=5,default='DV')
	temperature         = models.SmallIntegerField(default=0,blank=True,null=True)
	stowage             = models.CharField(max_length=10,blank=True,null=True
							,choices=STOWAGE_CHOICES)
	created             = models.DateTimeField(blank=True, null=True,auto_now_add=True)
	updated             = models.DateTimeField(blank=True, null=True,auto_now=True)
	status              = models.BooleanField(default=True)
	user 			    = models.ForeignKey(settings.AUTH_USER_MODEL,
							on_delete=models.CASCADE,
							blank=True,null=True,
							related_name = 'shorecontainers')

	def __str__(self):  # __unicode__ for Python 2
		return self.number

	def get_absolute_url(self):
		return reverse('shorepass:container-detail', kwargs={'pk': self.pk})
	
	class Meta:
		indexes = [
			models.Index(fields=['number'],name='idx_shore_container_number'),
		]

class Document(models.Model):
	shore               = models.ForeignKey(Shore,
							on_delete=models.CASCADE,
							blank=True, null=True,
							related_name = 'documents')
	shorefile           = models.ImageField(upload_to=image_file_name,blank=True, null=True)
	title               = models.CharField(max_length=100,blank=True,null=True)
	created             = models.DateTimeField(auto_now_add=True)




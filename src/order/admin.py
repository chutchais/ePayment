from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import date
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

# Register your models here.
from .models import Order,Container


# Added on Nov 5,2020 -- To support Export Order data and add filter by range
class OrderResource(resources.ModelResource):
	class Meta:
		model = Order
		import_id_fields = ()
		skip_unchanged = True
		report_skipped= True
		fields =('booking__terminal','booking__name','name','ref','grand_total','payment_date','payment_ref','user__username',
		'execute_by__username','execute_date','wht')
		exclude = ('id')


class OrderDateFilter(admin.SimpleListFilter):
	# Human-readable title which will be displayed in the
	# right admin sidebar just above the filter options.
	title = _('Order Created Date Range')

	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'created'

	def lookups(self, request, model_admin):
		"""
		Returns a list of tuples. The first element in each
		tuple is the coded value for the option that will
		appear in the URL query. The second element is the
		human-readable name for the option that will appear
		in the right sidebar.
		"""
		return (
			('today', _('Today')),
			('yesterday', _('Yesterday')),
			('thisweek', _('This week')),
			('lastweek', _('Last week')),
			('thismonth', _('This month')),
			('lastmonth', _('Last month')),
		)

	def queryset(self, request, queryset):
		"""
		Returns the filtered queryset based on the value
		provided in the query string and retrievable via
		`self.value()`.
		"""
		# Compare the requested value (either '80s' or '90s')
		# to decide how to filter the queryset.
		import datetime, pytz
		tz 			= pytz.timezone('Asia/Bangkok')
		today_tz 	=   datetime.datetime.now(tz=tz)

		from datetime import date
		if self.value() == 'today':
			today = today_tz#date.today()
			return queryset.filter(created__year=today.year,
								created__month=today.month,
								created__day=today.day).order_by('created')

		if self.value() == 'yesterday':
			import datetime
			# today = date.today() - datetime.timedelta(days=1)
			today = today_tz - datetime.timedelta(days=1)
			return queryset.filter(created__year=today.year,
								created__month=today.month,
								created__day=today.day).order_by('created')
		
		if self.value() == 'thisweek':
			import datetime
			date = today_tz #datetime.date.today()
			start_week = date - datetime.timedelta(date.weekday())
			end_week = start_week + datetime.timedelta(7)
			return queryset.filter(created__range=[start_week, end_week]).order_by('created')

		if self.value() == 'lastweek':
			import datetime
			date = today_tz#datetime.date.today()
			date_lastweek = date - datetime.timedelta(days=7)
			start_week = date_lastweek - datetime.timedelta(date_lastweek.weekday())
			end_week = start_week + datetime.timedelta(7)
			print (start_week, end_week)
			# date = end_week + datetime.timedelta(days=1)
			# start_week = date - datetime.timedelta(date.weekday())
			# end_week = start_week + datetime.timedelta(7)
			return queryset.filter(created__range=[start_week, end_week]).order_by('created')

		if self.value() == 'thismonth':
			today = today_tz #date.today()
			# print('this month')
			return queryset.filter(created__year=today.year,
								created__month=today.month).order_by('created')

		if self.value() == 'lastmonth':
			import datetime
			# today = date.today().replace(day=1) - datetime.timedelta(days=1)
			today = today_tz.replace(day=1) - datetime.timedelta(days=1)
			# print('last month',today)
			return queryset.filter(created__year=today.year,
								created__month=today.month).order_by('created')



class ContainerInline(admin.TabularInline):
	model = Container
	fields = ('container','cont_size','is_oog','total','invoice')
	readonly_fields = ('created','updated','user')
	extra = 0 # how many rows to show

	# autocomplete_fields = ('operation','next_pass','next_fail')
	show_change_link = True
	verbose_name = 'Container detail'
	verbose_name_plural = 'Container detail'

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','booking__name','qrid']
	list_filter = ['paid','execute_job','wht',OrderDateFilter]
	list_display = ('name','ref','booking','container_count','charge','vat_rate','wht','grand_total','paid',
					'seperate_bill','created','user')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user','vat_rate','wht_rate')
# 'lower_stock','higher_stock',
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True
	# filter_horizontal = ('childs',)

	fieldsets = [
		('Basic Information',{'fields': ['name','ref','booking','qrid','status']}),
		('Charge(s)',{'fields': ['charge',('vat_rate','wht_rate'),
								('wht','grand_total'),'seperate_bill']}),
		('WHT Slip',{'fields': ['wht_slip']}),
		('Payment',{'fields': ['address','paid','payment_date','payment_ref','payment_inspector']}),
		('Pay Slip',{'fields': ['payment_slip']}),
		('Execute job',{'fields': ['execute_job','execute_date','execute_by']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	inlines =[ContainerInline]
	resource_class      = OrderResource

# admin.site.register(Order)
# admin.site.register(Container)


# Added on Dec 7,2020 -- To support Export Container data and add filter by range
class ContainerResource(resources.ModelResource):
	class Meta:
		model = Container
		import_id_fields = ()
		skip_unchanged = True
		report_skipped= True
		fields = ('container','order__booking__name','cont_size','iso','is_oog','total','invoice',
					'created','user')
		exclude = ('id')

class ContainerDateFilter(admin.SimpleListFilter):
	# Human-readable title which will be displayed in the
	# right admin sidebar just above the filter options.
	title = _('Container Created Date Range')

	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'created'

	def lookups(self, request, model_admin):
		"""
		Returns a list of tuples. The first element in each
		tuple is the coded value for the option that will
		appear in the URL query. The second element is the
		human-readable name for the option that will appear
		in the right sidebar.
		"""
		return (
			('today', _('Today')),
			('yesterday', _('Yesterday')),
			('thisweek', _('This week')),
			('lastweek', _('Last week')),
			('thismonth', _('This month')),
			('lastmonth', _('Last month')),
		)

	def queryset(self, request, queryset):
		"""
		Returns the filtered queryset based on the value
		provided in the query string and retrievable via
		`self.value()`.
		"""
		# Compare the requested value (either '80s' or '90s')
		# to decide how to filter the queryset.
		import datetime, pytz
		tz 			= pytz.timezone('Asia/Bangkok')
		today_tz 	=   datetime.datetime.now(tz=tz)

		from datetime import date
		if self.value() == 'today':
			today = today_tz#date.today()
			return queryset.filter(created__year=today.year,
								created__month=today.month,
								created__day=today.day).order_by('created')

		if self.value() == 'yesterday':
			import datetime
			# today = date.today() - datetime.timedelta(days=1)
			today = today_tz - datetime.timedelta(days=1)
			return queryset.filter(created__year=today.year,
								created__month=today.month,
								created__day=today.day).order_by('created')
		
		if self.value() == 'thisweek':
			import datetime
			date = today_tz #datetime.date.today()
			start_week = date - datetime.timedelta(date.weekday())
			end_week = start_week + datetime.timedelta(7)
			return queryset.filter(created__range=[start_week, end_week]).order_by('created')

		if self.value() == 'lastweek':
			import datetime
			date = today_tz#datetime.date.today()
			date_lastweek = date - datetime.timedelta(days=7)
			start_week = date_lastweek - datetime.timedelta(date_lastweek.weekday())
			end_week = start_week + datetime.timedelta(7)
			print (start_week, end_week)
			# date = end_week + datetime.timedelta(days=1)
			# start_week = date - datetime.timedelta(date.weekday())
			# end_week = start_week + datetime.timedelta(7)
			return queryset.filter(created__range=[start_week, end_week]).order_by('created')

		if self.value() == 'thismonth':
			today = today_tz #date.today()
			# print('this month')
			return queryset.filter(created__year=today.year,
								created__month=today.month).order_by('created')

		if self.value() == 'lastmonth':
			import datetime
			# today = date.today().replace(day=1) - datetime.timedelta(days=1)
			today = today_tz.replace(day=1) - datetime.timedelta(days=1)
			# print('last month',today)
			return queryset.filter(created__year=today.year,
								created__month=today.month).order_by('created')


@admin.register(Container)
class ContainerAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['container','order__name']
	list_filter = ['cont_size','is_oog',ContainerDateFilter]
	list_display = ('container','order','cont_size','iso','is_oog','total','invoice',
					'created','user')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user','tariff')
# 'lower_stock','higher_stock',
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True
	# filter_horizontal = ('childs',)

	fieldsets = [
		('Basic Information',{'fields': ['container','order','cont_size','iso','is_oog']}),
		('Charge(s)',{'fields': [('tariff','total')]}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	resource_class      = ContainerResource

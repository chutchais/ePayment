from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from datetime import date


# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from .models import Shore,Document,Agent,Pod,Customer,Container

class DocumentInline(admin.TabularInline):
	model = Document
	fields = ('shorefile','title')
	readonly_fields = ('created',)
	extra = 0 # how many rows to show

	# autocomplete_fields = ('operation','next_pass','next_fail')
	# show_change_link = True
	verbose_name = 'Document detail'
	verbose_name_plural = 'Document detail'

class ContainerInline(admin.TabularInline):
	model = Container
	fields = ('number','cont_size','cont_type','temperature2','vent2','stowage')
	readonly_fields = ('created',)
	extra = 0 # how many rows to show

	# autocomplete_fields = ('operation','next_pass','next_fail')
	# show_change_link = True
	verbose_name = 'Container detail'
	verbose_name_plural = 'Container detail'

@admin.register(Shore)
class ShoreAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['booking','vessel_name','pod__name','voy','agent__name']
	list_filter = ['terminal','execute_job','need_contact',('execute_by', admin.RelatedOnlyFieldListFilter)]
	list_display = ('booking','terminal','agent','vessel_name','pod','voy','created','user','execute_job','execute_by')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','user')
# 'lower_stock','higher_stock',
	# save_as = True
	# save_as_continue = True
	# save_on_top =True
	list_select_related = True
	# filter_horizontal = ('childs',)

	fieldsets = [
		('Basic Information',{'fields': ['booking','terminal','agent']}),
		('Vessel Information',{'fields': ['vessel_name','pod','voy']}),
		('Customer Information',{'fields': ['customer']}),
		('Files Information',{'fields': ['shorefile1','shorefile2']}),
		('Need contact Information',{'fields': ['need_contact','message']}),
		('Execute job',{'fields': ['execute_job','execute_date','execute_by']}),
		('System Information',{'fields':[('user','created')]})
	]
	inlines =[DocumentInline,ContainerInline]
	# resource_class      = OrderResource


class PodResource(resources.ModelResource):
	class Meta:
		model = Pod
		import_id_fields = ('name',)
		skip_unchanged = True
		report_skipped= True
		exclude = ('id','user','created','updated','status' )


@admin.register(Pod)
class PodAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','description','actual_pod']
	list_filter = []
	list_display = ('name','description','actual_pod','created','user')
	readonly_fields = ('created','user')
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','description','actual_pod']}),
		('System Information',{'fields':[('user','created')]})
	]
	resource_class      = PodResource


class AgentResource(resources.ModelResource):
	class Meta:
		model = Agent
		import_id_fields = ('name',)
		skip_unchanged = True
		report_skipped= True
		exclude = ('id','user','created','updated','status' )

@admin.register(Agent)
class AgentAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','fullname']
	list_filter = []
	list_display = ('name','fullname','created','user')
	readonly_fields = ('created','user')
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','fullname']}),
		('System Information',{'fields':[('user','created')]})
	]
	resource_class      = AgentResource

class CustomerResource(resources.ModelResource):
	class Meta:
		model = Customer
		import_id_fields = ('name','tax',)
		skip_unchanged = True
		report_skipped= True
		exclude = ('id','user','created','updated','status' )

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['name','address','tax']
	list_filter = ['branch']
	list_display = ('name','address','tax','branch','created','user')
	readonly_fields = ('created','user')
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','address','tax','branch','description']}),
		('System Information',{'fields':[('user','created')]})
	]
	resource_class      = CustomerResource


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


class ContainerResource(resources.ModelResource):
	class Meta:
		model = Container
		import_id_fields = ()
		fields = ('number','shore__booking','shore__terminal','shore__vessel_name',
							'shore__agent','shore__voy','shore__pod','cont_size','temperature2',
							'vent2','stowage','created','shore__execute_date','shore__execute_by__username',)
		skip_unchanged = True
		report_skipped= True
		exclude = ('id','user','created','updated','status' )

@admin.register(Container)
class ContainerAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['number']
	list_filter = ['shore__terminal',ContainerDateFilter,'shore__execute_by']
	list_display = ('number','shore','cont_size','temperature2','vent2','stowage','created')
	readonly_fields = ('created','user')
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['number','shore','cont_size','temperature2','vent2','stowage']}),
		('System Information',{'fields':[('user','created')]})
	]
	resource_class      = ContainerResource

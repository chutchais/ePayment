from django.contrib import admin

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
	fields = ('number','cont_size','cont_type','temperature','vent2','stowage')
	readonly_fields = ('created',)
	extra = 0 # how many rows to show

	# autocomplete_fields = ('operation','next_pass','next_fail')
	# show_change_link = True
	verbose_name = 'Container detail'
	verbose_name_plural = 'Container detail'

@admin.register(Shore)
class ShoreAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin,admin.ModelAdmin):
	search_fields = ['booking','vessel_name','pod__name','voy','agent__name']
	list_filter = ['terminal','execute_job','need_contact']
	list_display = ('booking','terminal','agent','vessel_name','pod','voy','created','user','execute_job')
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

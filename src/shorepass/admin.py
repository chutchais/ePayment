from django.contrib import admin

# Register your models here.
from .models import Shore,Document,Agent,Pod

class DocumentInline(admin.TabularInline):
	model = Document
	fields = ('shorefile','title')
	readonly_fields = ('created',)
	extra = 0 # how many rows to show

	# autocomplete_fields = ('operation','next_pass','next_fail')
	# show_change_link = True
	verbose_name = 'Document detail'
	verbose_name_plural = 'Document detail'

@admin.register(Shore)
class ShoreAdmin(admin.ModelAdmin):
	search_fields = ['booking','vessel_name','pod__name','voy','agent__name']
	list_filter = ['terminal','execute_job']
	list_display = ('booking','agent','vessel_name','pod','voy','created','user','execute_job')
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
		('Customer Information',{'fields': ['customer_name']}),
		('Execute job',{'fields': ['execute_job','execute_date','execute_by']}),
		('System Information',{'fields':[('user','created')]})
	]
	inlines =[DocumentInline]
	# resource_class      = OrderResource


@admin.register(Pod)
class PodAdmin(admin.ModelAdmin):
	search_fields = ['name','description','actual_pod']
	list_filter = []
	list_display = ('name','description','actual_pod','created','user')
	readonly_fields = ('created','user')
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','description','actual_pod']}),
		('System Information',{'fields':[('user','created')]})
	]

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
	search_fields = ['name','fullname']
	list_filter = []
	list_display = ('name','fullname','created','user')
	readonly_fields = ('created','user')
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','fullname']}),
		('System Information',{'fields':[('user','created')]})
	]

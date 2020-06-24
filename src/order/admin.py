from django.contrib import admin

# Register your models here.
from .models import Order,Container


class ContainerInline(admin.TabularInline):
	model = Container
	fields = ('container','cont_size','is_oog','total')
	readonly_fields = ('created','updated','user')
	extra = 0 # how many rows to show

	# autocomplete_fields = ('operation','next_pass','next_fail')
	show_change_link = True
	verbose_name = 'Container detail'
	verbose_name_plural = 'Container detail'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	search_fields = ['name','ref','booking__name']
	list_filter = ['paid','execute_job']
	list_display = ('name','ref','booking','container_count','charge','vat_rate','grand_total','paid',
					'created','user')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user','vat_rate','wht_rate','wht')
# 'lower_stock','higher_stock',
	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True
	# filter_horizontal = ('childs',)

	fieldsets = [
		('Basic Information',{'fields': ['name','ref','booking','status']}),
		('Charge(s)',{'fields': ['charge',('vat_rate','wht_rate'),
								('wht','grand_total')]}),
		('Payment',{'fields': ['address','paid','payment_date','payment_ref','payment_inspector']}),
		('Pay Slip',{'fields': ['payment_slip']}),
		('Execute job',{'fields': ['execute_job','execute_date']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	inlines =[ContainerInline]

# admin.site.register(Order)
# admin.site.register(Container)

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
	search_fields = ['container','order__name']
	list_filter = ['cont_size','is_oog']
	list_display = ('container','order','cont_size','iso','is_oog','total',
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

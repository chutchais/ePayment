from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin
from .models import ContainerType,Tariff,ContainerProfile


@admin.register(ContainerProfile)
class ContainerProfileAdmin(admin.ModelAdmin):
	search_fields = []
	list_filter = ['category','full','oog','reef']
	list_display = ('category','full','oog','reef','note','status','created','updated','user')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user')

	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['category','full','oog','reef','note','status']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]

@admin.register(ContainerType)
class ContainerTypeAdmin(admin.ModelAdmin):
	search_fields = ['number','title']
	list_filter = []
	list_display = ('name','title','status','created','updated','user')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user')

	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['name','title','status']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	# inlines =[ProductInline,ProductStockInline,ProductImageInline]
	# resource_class      = ProductResource

# class TariffItemInline(admin.TabularInline):
# 	model 				= TariffItem
# 	fields 				= ('full','oog','size20','size40','size45','note')
# 	extra 				= 0
# 	show_change_link 	= True
# 	# autocomplete_fields = ['number']
# 	verbose_name 		= 'Tariff detail'
# 	verbose_name_plural = 'Tariff detail'

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
	search_fields = ['title']
	list_filter = ['container_profile']
	list_display = ('seq','title','container_profile','size20','size40','size45','status')
	# list_editable = ('color','move_performa')
	# autocomplete_fields = ['parent']
	readonly_fields = ('created','updated','user')

	save_as = True
	save_as_continue = True
	save_on_top =True
	list_select_related = True

	fieldsets = [
		('Basic Information',{'fields': ['seq','title','container_profile','status']}),
		('Tariff Information',{'fields': ['size20','size40','size45','note']}),
		('System Information',{'fields':[('user','created'),'updated']})
	]
	# inlines =[TariffItemInline]
from django.contrib import admin

# Register your models here.
from .models import Oog

class OogAdmin(admin.ModelAdmin):
    search_fields           = ['booking','container']
    list_display            = ('booking','container','created','user')
    readonly_fields         = ('created','user')
    fieldsets = [
        ('Basic Information',{'fields': ['booking','container']}),
        ('System Information',{'fields':['user','created']})
        ]
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(OogAdmin, self).save_model(request, obj, form, change)

admin.site.register(Oog,OogAdmin)

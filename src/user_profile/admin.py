from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile,Address

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class AddressInline(admin.TabularInline):
	model 				= Address
	fields 				= ('company','address','tax')
	extra 				= 0
	show_change_link 	= True
	verbose_name 		= 'Address Detail'
	verbose_name_plural = 'Addresses Detail'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, AddressInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# admin.site.register(User)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(Address)
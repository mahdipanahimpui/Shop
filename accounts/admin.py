from django.contrib import admin
from . models import User, OtpCode
from . forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


    

class UserAdmin(BaseUserAdmin):
     # you can customize the forms in the admin panel
     # creation/change form

    # the form name should be <form> and <add_form>
    form = UserChangeForm
    # adding another form
    add_form = UserCreationForm


    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name', 'password')}),
        ('Permision', {'fields': ('is_active', 'is_admin', 'is_superuser', 'user_permissions', 'groups','last_login')})
    ) # is for <form>

    add_fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name', 'pass1', 'pass2')}),
    )

    ordering = ('is_admin',)
    search_fields = ('email', 'full_name')
    filter_horizontal = ('groups', 'user_permissions') # for permisions,




# UnRegister the Group Model and Register your specific User Model
admin.site.register(User, UserAdmin)



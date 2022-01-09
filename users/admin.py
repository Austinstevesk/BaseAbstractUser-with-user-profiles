from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


#Displays the details of the users in the admin page instead of one field
class CustomUserAdmin(UserAdmin):
    list_display = ('email','first_name', 'last_name', 'phone', 'date_joined', 'last_login', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter=('last_login',)
    fieldsets = ()

    #Create the fields the user creation form should use since we removed the username field
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')
        }),
    )

    ordering = ('email',)



# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
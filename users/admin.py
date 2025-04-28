from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm # Optional: Use custom form in admin too

class CustomUserAdmin(UserAdmin):
    # Use the custom creation form if desired for adding users in admin
    # add_form = CustomUserCreationForm
    model = CustomUser
    # Add 'is_admin' to the list display and fieldsets to make it visible/editable
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

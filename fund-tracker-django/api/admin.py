from django.contrib import admin
from .models import Feedback

# Register the models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FundSource, Allocation, Proof

# This custom class is needed to show the 'role' field in the admin
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

admin.site.register(Feedback)

# Register all of the models here to make them visible
admin.site.register(User, CustomUserAdmin)
admin.site.register(FundSource)
admin.site.register(Allocation)
admin.site.register(Proof)

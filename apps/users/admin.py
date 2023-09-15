from django.contrib import admin
from .models import User, UserConfirmation


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number', 'email')


admin.site.register(User, UserAdmin)

admin.site.register(UserConfirmation)

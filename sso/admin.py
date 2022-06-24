from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "email", "status")

admin.site.register(User, UserAdmin)

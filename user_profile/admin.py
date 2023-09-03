from django.contrib import admin

from .models import User,Follow



class UserAdmin(admin.ModelAdmin):
    search_fields=('username',)
# Register your models here.

admin.site.register(User,UserAdmin)
admin.site.register(Follow)
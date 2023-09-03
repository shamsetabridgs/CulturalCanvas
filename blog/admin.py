from django.contrib import admin
from .models import *
from django.utils import timezone




admin.site.site_header = 'CULTURAL CANVAS Admin Panel'
admin.site.site_title = 'CulturalCanvasAdminPanel'
admin.site.index_title = ''

class BlogAdmin(admin.ModelAdmin):
    list_display=('user','title','created_date','category')
    list_filter=('user','category','title','created_date')
    search_fields=('user__username','title')
    list_display_links=('title',)

class CommentAdmin(admin.ModelAdmin):
    
    list_filter=('user','created_date')
    search_fields=('text','user__username',)

class ReportAdmin(admin.ModelAdmin):
    list_display=('name','link',)
    
    

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Reply)
admin.site.register(Report,ReportAdmin)
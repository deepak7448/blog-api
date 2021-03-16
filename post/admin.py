from django.contrib import admin
from .models import post,Comment
from django.utils.html import format_html

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('images' , )
    list_display = ('id','author','contents','created_on',)
    list_filter = ('author',)
    list_display_links=('id','author','contents',)
    search_fields = ['contents',]
    list_per_page = 20

    def contents(self,obj):
        return obj.content[:20]

    def images(self,obj):
        return format_html(f'<img src="http://127.0.0.1:8000/media/{obj.image}" style=width:300px>')
        
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','author','comment','reply','created_on')
    list_filter = ('author',)
    list_per_page = 20


admin.site.register(post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
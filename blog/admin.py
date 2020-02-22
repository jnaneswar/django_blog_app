from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin
#admin.site.register(Post)



class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title','date_posted','author')
    search_fields = ('title','content','author')
    list_filter = ('date_posted',)
admin.site.register(Post, PostAdmin)
from django.contrib import admin
from .models import Post, Comment, Tag, Like, File
# Register your models here.


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(File)

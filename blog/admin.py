from django.contrib import admin
from .models import Post, Author, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    list_filter = ('title', 'date', 'tags')
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)

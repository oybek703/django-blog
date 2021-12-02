from django.contrib import admin
from .models import Post, Author, Tags


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tags)

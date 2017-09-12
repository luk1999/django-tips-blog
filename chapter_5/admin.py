from django.contrib import admin

from chapter_5.models import Post


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(PostAdmin, Post)

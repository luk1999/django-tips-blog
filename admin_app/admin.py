from django.contrib import admin

from chapter_1.models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'text', 'published')
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('id', 'title', 'slug', 'created_at', 'published')


admin.site.register(Post, admin_class=PostAdmin)

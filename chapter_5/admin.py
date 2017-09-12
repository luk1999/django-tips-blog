from django.contrib import admin

from chapter_5.models import Result


class ResultAdmin(admin.ModelAdmin):
    pass


admin.site.register(Result, ResultAdmin)

from django.contrib import admin

from .models import Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ["pk", "word"]

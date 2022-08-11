from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'complete', 'created',)
    search_fields = ('user', 'title',)
    list_filter = ('complete', 'created',)


admin.site.register(Task, TaskAdmin)

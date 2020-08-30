from django.contrib import admin
from .models import ToDo

class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

# Register your models here.
admin.site.register(ToDo, ToDoAdmin)

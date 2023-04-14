from django.contrib import admin
from .models import New


class NewAdmin(admin.ModelAdmin):
    list_display = ('date', 'text_rus', 'text_eng', 'date_added')


admin.site.register(New, NewAdmin)
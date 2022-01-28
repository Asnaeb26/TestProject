from django.contrib import admin

from .models import *


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'user']
    list_editable = ['status']
    ordering = ['id']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'to_user', 'text']
    ordering = ['id']
    list_per_page = 10
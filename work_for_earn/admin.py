from django.contrib import admin
from .models import Work

class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'posted_by', 'accepted_by', 'payment_status')
    list_filter = ('category', 'status', 'payment_status')
    search_fields = ('title', 'description', 'posted_by__username', 'accepted_by__username')

admin.site.register(Work, WorkAdmin)

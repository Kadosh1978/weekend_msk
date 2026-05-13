from django.contrib import admin
from .models import PageVisit

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'path', 'country_name', 'device_type', 'browser_family', 'os_family', 'referrer', 'ip_address', 'first_seen')
    list_filter = ('device_type', 'browser_family', 'os_family', 'country_name', 'first_seen')
    search_fields = ('session_key', 'path', 'referrer', 'ip_address', 'country_name')
    readonly_fields = ('first_seen',)
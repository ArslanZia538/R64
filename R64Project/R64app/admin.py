from django.contrib import admin
from .models import History, Cash

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('reciever', 'giver', 'amount', 'event', 'date', 'status')

class CashAdmin(admin.ModelAdmin):
    list_display = ('reciever', 'giver', 'amount', 'event', 'date', 'status')

admin.site.register(History, HistoryAdmin)
admin.site.register(Cash, CashAdmin)


admin.site.site_header = "R64 Cash-Counter"
from django.contrib import admin
from .models import AdvisorSummary, ClientSummary, Transaction

@admin.register(ClientSummary)
class ClientSummaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'broker')  
    list_filter = ('broker',)
    search_fields = ('name',)
    ordering = ('name', 'broker')
    def display_total(self, obj):
        return obj.calculate_total()
    display_total.short_description = 'Total'
    
@admin.register(AdvisorSummary)
class AdvisorSummaryAdmin(admin.ModelAdmin):
    list_display = ('total_equity', 'average_equity', 'total_clients')
    ordering = ('-total_equity',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    def client_name(self, obj):
        return obj.client.name
    client_name.admin_order_field = 'client__name' 
    client_name.short_description = 'Client Name'  
    list_display = ('client_name', 'date', 'value', 'transaction_type')
    list_filter = ('transaction_type', 'client__broker')
    search_fields = ('client__name',)
    ordering = ('-date',) 
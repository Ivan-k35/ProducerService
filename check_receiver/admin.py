from django.contrib import admin
from .models import PurchaseCheck, Item


@admin.register(PurchaseCheck)
class PurchaseCheckAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'timestamp', 'total_amount', 'payment_method']
    list_filter = ['timestamp', 'payment_method']
    search_fields = ['transaction_id', 'place_name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'quantity', 'price', 'category', 'purchase_check']
    list_filter = ['category']
    search_fields = ['product_id', 'purchase_check__transaction_id']

from django.contrib import admin
from .models import Product, Order, OrderItem, Profile, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'created')
    inlines = [OrderItemInline]


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile)
admin.site.register(ShippingAddress)

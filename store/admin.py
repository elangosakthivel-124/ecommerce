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

from django.contrib import admin
from .models import Product, Order, OrderItem, Profile, ShippingAddress, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(ShippingAddress)


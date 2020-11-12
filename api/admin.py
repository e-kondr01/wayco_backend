from django.contrib import admin
from .models import *


class OrderedProductInline(admin.StackedInline):
    model = OrderedProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at',)
    inlines = [OrderedProductInline]


admin.site.register(Cafe)
admin.site.register(CafePhoto)
admin.site.register(Product)
admin.site.register(ProductOption)
admin.site.register(ProductOptionChoice)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedProduct)
admin.site.register(Consumer)
admin.site.register(CafeRating)
admin.site.register(Employee)

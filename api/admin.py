from django.contrib import admin
from .models import *


class OrderedProductInline(admin.StackedInline):
    model = OrderedProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at',)
    inlines = [OrderedProductInline]


class ProductOptionInline(admin.StackedInline):
    model = ProductOption
    extra = 1
    show_change_link = True


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductOptionInline]


class ProductOptionChoiceInline(admin.StackedInline):
    model = ProductOptionChoice
    extra = 1
    show_change_link = True


class ProductOptionAdmin(admin.ModelAdmin):
    inlines = [ProductOptionChoiceInline]


admin.site.register(Cafe)
admin.site.register(CafePhoto)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)
admin.site.register(ProductOptionChoice)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedProduct)
admin.site.register(Consumer)
admin.site.register(CafeRating)
admin.site.register(Employee)

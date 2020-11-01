from django.contrib import admin
from .models import *


admin.site.register(Cafe)
admin.site.register(CafePhoto)
admin.site.register(Product)
admin.site.register(ProductOption)
admin.site.register(ProductOptionChoice)
admin.site.register(Order)
admin.site.register(OrderedProduct)
admin.site.register(Consumer)

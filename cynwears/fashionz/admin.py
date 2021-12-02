from django.contrib import admin
from .models import Product,Category,Order,Orderitem,Subcategory,Rating

# Register your models here.

admin.site.register(Subcategory)
# admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(Rating)

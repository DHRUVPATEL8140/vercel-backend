# products/admin.py
from django.contrib import admin
from .models import Product, Order, CompanyInfo, Pillow, EPESheet

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","density","size","price","stock")
    search_fields = ("name","description")
    list_filter = ("color",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","user","total_amount","created_at","paid")
    readonly_fields = ("created_at",)

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("name","contact_email")


@admin.register(Pillow)
class PillowAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock")   
    search_fields = ("name", "description")
    list_filter = ("color",)   


@admin.register(EPESheet)
class EPESheetAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "size", "created_at")
    search_fields = ("name", "description")
    list_filter = ("size", "created_at")

from django.contrib import admin
from store import  models as models
from store.models import Category, Product, Variant, VariantItem, Gallery, Cart, Coupon, Order, OrderItem, Review

class GalleryInline(admin.TabularInline):
    model = models.Gallery

class VariantInline(admin.TabularInline):
    model = models.Variant

class VariantItemInline(admin.TabularInline):
    model = models.VariantItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    list_editable = ['image']
    prepopulated_fields = {'slug': ('title',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'status', 'stock', 'featured', 'vendor', 'date']
    search_fields = ['name', 'category__title']
    list_filter = ['status', 'featured', 'category']
    inlines = [GalleryInline, VariantInline]
    populated_fields = {'slug': ('name',)}

class VariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name']
    inlines = [VariantItemInline]

class VariantItemAdmin(admin.ModelAdmin):
    list_display = ['variant', 'title', 'content']
    search_fields = ['variant__name', 'title']

class GalleryAdmin(admin.ModelAdmin):
    list_display = ['product', 'gallery_id']
    search_fields = ['product__name', 'gallery_id']

class CartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'qty', 'price','total','date']
    search_fields = ['cart_id','product__name', 'user__username']
    list_filter = ['date', 'product']

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'vendor']
    search_fields = ['code','vendor_username']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'payment_status','order_status','payment_method', 'date']
    search_fields = ['order_id', 'customer__username']
    list_filter = ['payment_status', 'order_status']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item_id','order', 'product','qty', 'price', 'total']
    search_fields = ['item_id','order__order_id', 'product__name']
    list_filter = ['order__date']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating','active', 'date']
    search_fields = ['product__name','user__username']
    list_filter = ['active', 'rating']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(VariantItem, VariantItemAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Review, ReviewAdmin)














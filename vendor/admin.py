from django.contrib import admin
from vendor.models import Vendor, Payout, BankAccount, Notification


class VendorAdmin(admin.ModelAdmin):
    list_display = ['store_name','vendor_id', 'user', 'date']
    search_fields = ['store_name', 'user__username','vendor_id']
    prepopulated_fields = {'slug': ('store_name',)}
    list_filter = ['date']


class PayoutAdmin(admin.ModelAdmin):
    list_display = ['payout_id','vendor','item','amount','date']
    search_fields = ['payout_id','vendor__store_name','item__order__order_id']
    list_filter = ['date','vendor']

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['vendor','bank_name','account_number','account_type']
    search_fields = ['vendor__store_name','bank_name','account_number','account_name']
    list_filter = ['bank_name','account_type']    

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user','type','order','seen']
    list_editable = ['order']

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Payout, PayoutAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Notification, NotificationAdmin)









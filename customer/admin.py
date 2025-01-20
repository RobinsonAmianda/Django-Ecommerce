from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from customer.models import Address, Wishlist,Notification

class AddressAdmin(ImportExportModelAdmin):
    list_display = ['user','full_name']

class WishlistAdmin(ImportExportModelAdmin):
    list_display = ['user','product']

class NotificationAdmin(ImportExportModelAdmin):
    list_display = ['user','type','seen','date']

admin.site.register(Address , AddressAdmin)
admin.site.register(Wishlist , WishlistAdmin)
admin.site.register(Notification, NotificationAdmin)








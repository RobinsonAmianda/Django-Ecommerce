from django.db import models
from shortuuid.django_fields import ShortUUIDField
from user_auth.models import User
from django.utils.text import slugify

NOTIFICATION_TYPE = (
    ('New Order', 'New Order'),
    ('New Review', 'New review'),
)

PAYMENT_METHOD = (
    ('M-Pesa', 'M-Pesa'),
    ('Paypal', 'Paypal'),
    ('Stripe', 'Stripe'),
)

TYPE = (
    ('New Order', 'New Order'),
    ('Item Shipped', 'Item Shipped'),
    ('Item Delivered', 'Item Delivered'),
)

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images',default='shop-image.jpg', blank    =True)
    store_name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    vendor_id = ShortUUIDField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True,null =True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.store_name)
        super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.store_name
    
class Payout(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey('store.OrderItem', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    payout_id = ShortUUIDField(unique=True,length=6,max_length=10,alphabet ='1234567890')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor
    
class BankAccount(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    account_type = models.CharField(max_length=255,choices=PAYMENT_METHOD,null=True,blank=True)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    bank_code = models.CharField(max_length=255)
    stripe_id = models.CharField(max_length=255,null=True,blank=True)
    paypal_address = models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Bank Accounts'
    def __str__(self):
        return self.bank_name
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True,related_name='vendor_notifications')
    type = models.CharField(max_length=50, choices=TYPE, default=None)
    order = models.ForeignKey('store.OrderItem', on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Notification'

    def __str__(self):
        return self.type
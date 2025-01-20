from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
import shortuuid
from user_auth import models as user_models

STATUS = (
    ('Published', 'Published'), 
    ('Draft', 'Draft'),
    ('Disabled', 'Disabled')
)

PAYMENT_STATUS = (
    ('Paid', 'Paid'),
    ('Processing', 'Processing'),
    ('Failed', 'Failed')
)

PAYMENT_METHOD = (
    ('Paypal', 'Paypal'),
    ('Stripe', 'Stripe'),
    ('M-Pesa', 'M-Pesa')
)

SHIPPING_SERVICES = (
    ('DHL', 'DHL'),
    ('Fedx', 'Fedx'),
    ('UPS', 'UPS'),
    ('GIG Logistics', 'GIG Logistics')
)

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Fulfilled', 'Fulfilled'),
    ('Cancelled', 'Cancelled')
)

RATING = (
    (1, '★☆☆☆☆'), 
    (2, '★★☆☆☆'),  
    (3, '★★★☆☆'),  
    (4, '★★★★☆'),  
    (5, '★★★★★')  
)

class Category(models.Model):  # Add models.Model here
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image', blank=True, null=True) 
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    description = CKEditor5Field()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)  # Correct reference
    price = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2, verbose_name='Sale Price')
    regular_price = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2, verbose_name='Regular Price')
    stock = models.PositiveIntegerField(default=0, null=True, blank=True)
    shipping = models.DecimalField(default=0, null=True, blank=True, verbose_name='Shipping Amount', decimal_places=2,max_digits=10)
    status = models.CharField(max_length=255, choices=STATUS, default='Published')
    featured = models.BooleanField(default=False, verbose_name='MarketPlace Featured')
    vendor = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    sku = ShortUUIDField(unique=True, length=5, alphabet='1234567890', prefix='SKU')
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + '-' + str(shortuuid.uuid().lower()[:2])
        super(Product, self).save(*args, **kwargs)


class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255,null=True, blank=True)

    def items(self):
        return VariantItem.objects.filter(variant=self)
    def __str__(self):
        return self.name

class VariantItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_items')
    title = models.CharField(max_length=255, verbose_name= 'Item Title', blank=True, null=True)
    content  =models.CharField(max_length=2550 , verbose_name= 'Item Content', blank=True, null=True)

    def __str__(self):
        return self.variant.name

class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images',default='gallery.jpg')
    gallery_id = ShortUUIDField(unique=True, length= 5, alphabet = '1234567890', prefix = 'GID')

    def __str__(self):
        return f'{self.product.name} + image'
    class Meta:
        verbose_name_plural = 'Gallery'
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    qty = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    tax = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    total = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    size =models.CharField(max_length=255, blank=True, null=True)
    color =models.CharField(max_length=255, blank=True, null=True)
    cart_id = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.cart_id} - {self.product.name}'
    

class Coupon(models.Model):
    vendor = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=255)
    discount = models.IntegerField(default=1)

    def __str__(self):
        return self.code
    
class Order(models.Model):
    vendors = models.ManyToManyField('user_auth.User', blank=True,  related_name='vendor_orders')
    customer = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_orders')
    sub_total=models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    shipping = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    tax = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    service_fee  = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS, default='Processing')
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD, default='None', blank=True, null=True)
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS, default='Pending')
    initial_total = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2,help_text='Total amount before discount')
    saved = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2,help_text='Total amount saved')
    # address = models.ForeignKey('customer.Address', on_delete=models.SET_NULL, null=True, blank=True)
    coupons = models.ManyToManyField('Coupon', blank=True)
    order_id = ShortUUIDField(unique=True, length= 5, alphabet = '1234567890', prefix = 'OID')
    payment_id = models.CharField(max_length=2000, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Orders'
    def __str__(self):
        return f'{self.order_id} - {self.customer.first_name}'
    
    def order_items(self):
        return OrderItem.objects.filter(order=self)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS, default='Pending')
    shipping_service  = models.CharField(max_length=255, choices=SHIPPING_SERVICES, default='DHL')
    tracking_id = models.CharField(max_length=255, default=None, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    tax = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    total = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    initial_total = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    saved = models.DecimalField(max_digits=10, default=0.00, null=True, blank=True, decimal_places=2)
    coupon = models.ManyToManyField("Coupon", blank=True)
    applied_coupon = models.BooleanField(default=False)
    item_id = ShortUUIDField(unique=True, length= 5, alphabet = '1234567890', prefix = 'IID')
    vendor = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def order_id(self):
        return self.order.order_id
    def __str__(self):
        return f'{self.item_id} - {self.product.name}'
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Order Items'


class Review(models.Model):
    user = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'reviews')
    review = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(choices=RATING, default=None)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} review on {self.product.name}'

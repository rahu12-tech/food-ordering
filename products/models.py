from django.db import models 
from django.contrib.auth.models import User 
from django.db.models import Sum
import uuid

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(unique=True)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_demo_price = models.IntegerField(default=0)
    quantity = models.CharField(max_length=50, null=True, blank=True)
    product_images = models.ImageField(upload_to="products")

class ProductMetaInformation(BaseModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="meta_information")
    product_measuring = models.CharField(max_length=100, null=True, blank=True, choices=(("KG", "KG"), ("ML", "ML"), ("L", "L"), (None, None)))
    product_quantity = models.CharField(max_length=50, null=True, blank=True)
    is_restrict = models.BooleanField(default=False)
    restrict_quantity = models.IntegerField()

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="carts")
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        return CartItems.objects.filter(cart = self).aggregate(Sum('product__product_price'))['product__product_price__sum']

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    


    
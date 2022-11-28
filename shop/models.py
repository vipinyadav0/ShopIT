
from re import T
from tabnanny import verbose
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.shortcuts import reverse


# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    address = models.CharField(max_length=40, null=True, blank=True)
    mobile = models.CharField(max_length=20,null=True, blank=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.username
    
    @property
    def get_by_username(self):
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=100,null=True, blank=True)
    category = models.ForeignKey("Category", null=False,blank= False, on_delete=models.CASCADE)
    original_price = models.FloatField(null=False, blank=False)
    discount_price = models.FloatField(null=True, blank= True)
    image = models.ImageField(upload_to='product_image/', null = True, blank =True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)
    
    def get_context_data(self, **kwargs):
        context = super(Product, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context  



class Category(models.Model):
    category = models.CharField(max_length=50, null=False, blank= False)

    def __str__(self) -> str:
        return self.category

    class Meta:
        verbose_name = "Categorie"
    

class Order(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    price = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)

    stripe_payment_intent = models.CharField(
        max_length=200
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )



class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name



# def userprofile_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         userprofile = UserProfile.objects.create(user=instance)


# post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=15, null=True, blank=True, default='India')
    state = models.CharField(max_length=10, null=True, blank=True)
    post_code = models.IntegerField(max_length=6, null=True, blank=True)
    save_info = models.BooleanField(default="True", null=True, blank=True)


    class Meta:
        verbose_name = ("ShippingAddress")
        verbose_name_plural = ("ShippingAddresss")

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("ShippingAddress_detail", kwargs={"pk": self.pk})

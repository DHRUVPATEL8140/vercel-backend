# products/models.py
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    density = models.FloatField(help_text="kg/m3 or unit your company uses")
    size = models.CharField(max_length=100)  # e.g., 6x4x1 inch or custom
    color = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.JSONField()  # list of {product_id, name, qty, price}
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.TextField()
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class CompanyInfo(models.Model):
    name = models.CharField(max_length=200, default="Infinite Private Limited")
    description = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    product = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.name} for {self.product}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="1-5 stars")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'user']   
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"



# products/models.py
class Pillow(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)  
    stock = models.PositiveIntegerField(default=0)   
    image = models.ImageField(upload_to='pillows/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class EPESheet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='epesheets/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

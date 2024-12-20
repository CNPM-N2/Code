# QuanLyDonHang/models.py  

from django.db import models  

class Product(models.Model):  
    name = models.CharField(max_length=100)  
    barcode = models.CharField(max_length=50, unique=True)  
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)  
    weight = models.DecimalField(max_digits=5, decimal_places=2)  
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2)  

    def __str__(self):  
        return self.name  

class Order(models.Model):  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField()  
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  

    def save(self, *args, **kwargs):  
        # Tính giá bán  
        self.total_price = self.product.cost_price * self.quantity * (1 + self.product.markup_percentage / 100)  
        super().save(*args, **kwargs)  

    def __str__(self):  
        return f"Order {self.id}: {self.product.name} x {self.quantity}"
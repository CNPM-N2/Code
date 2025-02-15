from django.db import models
from django.contrib.auth.models import User

class Repurchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang chờ'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
        ('completed', 'Hoàn thành'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Khách hàng")
    product_name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    product_code = models.CharField(max_length=50, verbose_name="Mã sản phẩm")
    quantity = models.IntegerField(default=1, verbose_name="Số lượng")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tổng tiền")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    def save(self, *args, **kwargs):
        self.total_amount = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.username} - {self.product_name}"

    class Meta:
        verbose_name = "Yêu cầu mua lại"
        verbose_name_plural = "Yêu cầu mua lại"
        ordering = ['-created_at']

class RepurchaseHistory(models.Model):
    repurchase = models.ForeignKey(Repurchase, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=50, verbose_name="Hành động")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian")
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Người thực hiện"
    )

    def __str__(self):
        return f"{self.repurchase} - {self.action}"

    class Meta:
        verbose_name = "Lịch sử mua lại"
        verbose_name_plural = "Lịch sử mua lại"
        ordering = ['-created_at']
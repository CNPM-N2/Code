from django.db import models

# Create your models here.

# Danh mục sản phẩm (VD: Nhẫn, Dây chuyền, Bông tai)
class DanhMuc(models.Model):
    ten = models.CharField(max_length=255)

    def __str__(self):
        return self.ten

# Thông tin về loại vàng
class Vang(models.Model):
    LOAI_VANG_CHOICES = [
        ('24K', 'Vang 24K'),
        ('18K', 'Vang 18K'),
        ('14K', 'Vang 14K'),
    ]
    loai = models.CharField(max_length=10, choices=LOAI_VANG_CHOICES)
    gia_hien_tai = models.DecimalField(max_digits=10, decimal_places=2)  # Giá theo thời điểm

    def __str__(self):
        return f"{self.loai} - {self.gia_hien_tai} VND"

# Thông tin về các loại đá quý đi kèm sản phẩm
class ChiTietDa(models.Model):
    ten = models.CharField(max_length=255)
    gia_mua_lai = models.DecimalField(max_digits=10, decimal_places=2)  # Giá mua lại (VD: 70% giá ban đầu)

    def __str__(self):
        return self.ten

# Thông tin sản phẩm trang sức
class SanPham(models.Model):
    ten = models.CharField(max_length=255)
    danh_muc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE)  # Liên kết với DanhMuc
    vang = models.ForeignKey(Vang, on_delete=models.CASCADE)  # Liên kết với Vang
    chi_tiet_da = models.ManyToManyField(ChiTietDa, blank=True)  # Nhiều loại đá quý
    trong_luong = models.FloatField()  # Trọng lượng (gam)
    tien_cong = models.DecimalField(max_digits=10, decimal_places=2)  # Tiền công chế tác
    gia_von = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Giá vốn
    gia_ban = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Giá bán
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def tinh_gia_von(self):
        return (self.vang.gia_hien_tai * self.trong_luong) + self.tien_cong

    def tinh_gia_ban(self):
        return self.gia_von * 1.2  # Ví dụ: nhân 1.2 để có giá bán

    def save(self, *args, **kwargs):
        self.gia_von = self.tinh_gia_von()
        self.gia_ban = self.tinh_gia_ban()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ten} - {self.vang.loai}"

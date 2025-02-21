from django.db import models
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from django.contrib.auth.models import User

class DanhMuc(models.Model):
    ten_danh_muc = models.CharField(max_length=100)

    def __str__(self):
        return self.ten_danh_muc

# Người Dùng
class NguoiDung(models.Model):
    GIOI_TINH_CHOICES = [
        ('Nam', 'Nam'),
        ('Nu', 'Nữ'),
    ]
    ten_dang_nhap = models.CharField(max_length=50, unique=True)
    mat_khau = models.CharField(max_length=100)
    ho_ten = models.CharField(max_length=100)
    ngay_sinh = models.DateField()
    gioi_tinh = models.CharField(
        max_length=3,
        choices=GIOI_TINH_CHOICES,
        default='Nam'
    )
    sdt = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

# Vai Trò
class VaiTro(models.Model):
    ma_nv = models.CharField(max_length=20)
    chuc_vu = models.CharField(max_length=100)

# Nhân Viên
class NhanVien(models.Model):
    id = models.AutoField(primary_key=True)
    nguoi_dung = models.OneToOneField('NguoiDung', on_delete=models.CASCADE)
    vai_tro = models.ForeignKey(VaiTro, on_delete=models.CASCADE)

# Quầy
class Quay(models.Model):
    ma_quay = models.CharField(max_length=20, primary_key=True)
    so_quay = models.CharField(max_length=20)

# Doanh Thu Nhân Viên
class DoanhThuNhanVien(models.Model):
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    ngay = models.DateField()
    doanh_thu = models.FloatField()

# Doanh Thu Quầy
class DoanhThuQuay(models.Model):
    quay = models.ForeignKey(Quay, on_delete=models.CASCADE)
    ngay = models.DateField()
    doanh_thu = models.FloatField()

# Đá
class Da(models.Model):
    ma_da = models.CharField(max_length=20, primary_key=True)
    ten_da = models.CharField(max_length=50)
    mau_sac = models.CharField(max_length=30)
    carat = models.FloatField()
    gia_ban = models.FloatField()

    def __str__(self):
        return self.ten_da

# Chi Tiết Đơn Mua/Bán
class ChiTietDon(models.Model):
    ma_don = models.CharField(max_length=20)
    san_pham = models.ForeignKey('SanPham', on_delete=models.CASCADE)
    so_luong = models.PositiveIntegerField()

# Sản Phẩm
class SanPham(models.Model):
    ma_sp = models.CharField(max_length=20, primary_key=True)
    ten_sp = models.CharField(max_length=100)
    trong_luong = models.FloatField()
    gia_ban = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    da = models.ManyToManyField(Da, through='ChiTietDa')
    danh_muc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE)
    mo_ta = models.CharField(max_length=250, default='', null=True, blank=True)
    hinh_anh = models.ImageField(upload_to='product/', blank=True, null=True)    #image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.ten_sp
    @property
    def ImageURL(self):
        if self.hinh_anh and hasattr(self.hinh_anh, 'url'):
            return self.hinh_anh.url
        return '/static/images/Jewelry-Images/products/default.jpg'

class Order(models.Model):   
    customer = models.ForeignKey(NguoiDung,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
class OrderItem(models.Model):   
    product = models.ForeignKey(SanPham,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.gia_ban * self.quantity
        return total
class ShippingAddress(models.Model):   
    customer = models.ForeignKey(NguoiDung,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    mobile = models.CharField(max_length=10,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
           return self.address

class ChiTietDa(models.Model):
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    da = models.ForeignKey(Da, on_delete=models.CASCADE)
    so_luong = models.IntegerField()

# Đơn Bán
class DonBan(models.Model):
    ma_db = models.CharField(max_length=20, primary_key=True)
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    ngay_ban = models.DateField()
    tong_tien = models.FloatField()

# Đơn Mua
class DonMua(models.Model):
    ma_dm = models.CharField(max_length=20, primary_key=True)
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    ngay_mua = models.DateField()
    tong_don_mua = models.FloatField()

# Khuyến Mãi và Ưu Đãi
class KhuyenMai(models.Model):
    ma_km = models.CharField(max_length=20, primary_key=True)
    loai = models.CharField(max_length=100)
    ngay_bat_dau = models.DateField()
    ngay_ket_thuc = models.DateField()
    chiet_khau = models.FloatField()

class UuDai(models.Model):
    ma_uu_dai = models.CharField(max_length=20, primary_key=True)
    loai = models.CharField(max_length=100)
    diem_tich_luy = models.FloatField()
    chiet_khau = models.FloatField()

# Bảo Hành
class ChinhSachBaoHanh(models.Model):
    ma_bh = models.CharField(max_length=20, primary_key=True)
    don_ban = models.ForeignKey(DonBan, on_delete=models.CASCADE)
    mo_ta = models.TextField()
    thoi_gian_bao_hanh = models.PositiveIntegerField()

class Vang(models.Model):
    ma_vang = models.CharField(max_length=20, primary_key=True)
    loai_vang = models.CharField(max_length=50)

    gia_mua = models.FloatField()
    gia_ban = models.FloatField()
    ngay_cap_nhat = models.DateField(auto_now=True)
  
    def __str__(self):
        return self.loai_vang

class LichSuGiaVang(models.Model):
    vang = models.ForeignKey(Vang, on_delete=models.CASCADE)
    ngay = models.DateField()
    gia_mua = models.FloatField()
    gia_ban = models.FloatField()
    
    class Meta:
        unique_together = ('vang', 'ngay')

class HoSoKhachHang(models.Model):
    GIOI_TINH_CHOICES = [
        ('Nam', 'Nam'),
        ('Nu', 'Nữ'),
    ]
    ma_khach = models.CharField(max_length=20, primary_key=True)
    ho_ten = models.CharField(max_length=100)
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE)
    ngay_sinh = models.DateField()
    gioi_tinh = models.CharField(
        max_length=3,
        choices=GIOI_TINH_CHOICES,
        default='Nam'
    )
    diem_tich_luy = models.IntegerField()
    sdt = models.CharField(max_length=15)
    email = models.EmailField()
    dia_chi = models.CharField(max_length=200)

    def __str__(self):
        return self.ho_ten
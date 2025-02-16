# core/models.py
from django.db import models

# Người Dùng
class NguoiDung(models.Model):
    ten_dang_nhap = models.CharField(max_length=50, unique=True)
    mat_khau = models.CharField(max_length=100)
    ho_ten = models.CharField(max_length=100)
    ngay_sinh = models.DateField()
    gioi_tinh = models.BooleanField()
    sdt = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

# Vai Trò
class VaiTro(models.Model):
    ma_nv = models.CharField(max_length=20)
    chuc_vu = models.CharField(max_length=100)

# Nhân Viên
class NhanVien(models.Model):
    id = models.AutoField(primary_key=True)
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE)
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
    gia_ban = models.FloatField()
    da = models.ManyToManyField(Da, through='ChiTietDa')

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
    ma_khach = models.CharField(max_length=20, primary_key=True)
    ho_ten = models.CharField(max_length=100)
    nguoi_dung = models.OneToOneField(NguoiDung, on_delete=models.CASCADE)
    ngay_sinh = models.DateField()
    gioi_tinh = models.BooleanField()
    diem_tich_luy = models.IntegerField()
    sdt = models.CharField(max_length=15)
    email = models.EmailField()
    dia_chi = models.CharField(max_length=200)

    def __str__(self):
        return self.ho_ten
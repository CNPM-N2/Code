from django.contrib import admin
from .models import *
class ChiTietDaInline(admin.TabularInline):
    model = ChiTietDa
    extra = 1
class SanPhamAdmin(admin.ModelAdmin):
    list_display = ['ma_sp', 'ten_sp', 'trong_luong', 'gia_ban']
    inlines = [ChiTietDaInline]

admin.site.register(DanhMuc)
admin.site.register(NguoiDung)
admin.site.register(SanPham, SanPhamAdmin)
admin.site.register(Vang)
admin.site.register(Da)
admin.site.register(HoSoKhachHang)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
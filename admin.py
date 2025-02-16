from django.contrib import admin

# Register your models here.
from .models import SanPham, DanhMuc, Vang, ChiTietDa

admin.site.register(SanPham)
admin.site.register(DanhMuc)
admin.site.register(Vang)
admin.site.register(ChiTietDa)

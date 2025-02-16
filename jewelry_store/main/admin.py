from django.contrib import admin
from .models import Product
from .models import SanPham, DanhMuc, Vang, ChiTietDa

admin.site.register(Product)

admin.site.register(SanPham)
admin.site.register(DanhMuc)
admin.site.register(Vang)
admin.site.register(ChiTietDa)
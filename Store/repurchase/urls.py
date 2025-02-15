from django.urls import path
from . import views

app_name = 'repurchase'

urlpatterns = [
    path('', views.repurchase_list, name='list'),
    path('create/', views.create_repurchase, name='create'),
    path('detail/<int:pk>/', views.repurchase_detail, name='detail'),
]
import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ShoppingCart } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';

const ProductCard = ({ product, onAddToCart, isAuthenticated }) => {
  const { toast } = useToast();

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      window.location.href = '/login/';
      return;
    }

    try {
      const response = await fetch('/update_item/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          productId: product.ma_sp,
          action: 'add'
        })
      });

      if (response.ok) {
        toast({
          title: "Thành công",
          description: "Đã thêm sản phẩm vào giỏ hàng",
        });
        window.location.href = '/cart/';
      } else {
        throw new Error('Failed to add to cart');
      }
    } catch (error) {
      toast({
        title: "Lỗi",
        description: "Không thể thêm vào giỏ hàng. Vui lòng thử lại sau.",
        variant: "destructive"
      });
    }
  };

  return (
    <Card className="w-full">
      <CardContent className="p-4">
        <a href={`/product/${product.ma_sp}/`} className="block">
          <img 
            src={product.ImageURL} 
            alt={product.ten_sp} 
            className="w-full h-48 object-cover rounded-lg mb-4"
          />
          <h3 className="font-semibold text-lg mb-2 line-clamp-2">{product.ten_sp}</h3>
          <p className="text-gray-600 mb-4">{parseInt(product.gia_ban).toLocaleString()} VNĐ</p>
        </a>
        <Button 
          className="w-full bg-blue-600 hover:bg-blue-700"
          onClick={handleAddToCart}
        >
          <ShoppingCart className="w-4 h-4 mr-2" />
          Thêm vào giỏ
        </Button>
      </CardContent>
    </Card>
  );
};

const ProductGrid = ({ initialData }) => {
  const { products, isAuthenticated } = initialData;

  return (
    <div className="max-w-7xl mx-auto p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.map((product) => (
          <ProductCard
            key={product.ma_sp}
            product={product}
            isAuthenticated={isAuthenticated}
          />
        ))}
      </div>
    </div>
  );
};

const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

export { ProductCard, ProductGrid };
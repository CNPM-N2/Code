import React, { useState } from 'react';
import { ShoppingCart, Trash2 } from 'lucide-react';
import { Alert, AlertTitle } from '@/components/ui/alert';

const CartComponent = () => {
  const [showAlert, setShowAlert] = useState(false);

  const updateCart = (productId, action) => {
    if (!user) {
      window.location.href = '/login/';
      return;
    }

    fetch('/update_cart/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        productId: productId,
        action: action,
      }),
    })
    .then(response => response.json())
    .then(data => {
      setShowAlert(true);
      setTimeout(() => setShowAlert(false), 3000);
      location.reload();
    });
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

  return (
    <div className="relative">
      {showAlert && (
        <Alert className="fixed top-4 right-4 w-72 bg-green-100 border-green-400">
          <AlertTitle>Giỏ hàng đã được cập nhật!</AlertTitle>
        </Alert>
      )}
      
      <div className="cart-icon">
        <ShoppingCart className="h-6 w-6" />
        <span className="cart-count">0</span>
      </div>

      <div className="cart-content">
        <div className="cart-header">
          <h3 className="text-lg font-semibold">Giỏ hàng của bạn</h3>
        </div>
        
        <div className="cart-items">
        </div>

        <div className="cart-footer">
          <div className="flex justify-between items-center p-4 border-t">
            <span className="font-semibold">Tổng cộng:</span>
            <span className="text-xl font-bold">0 VNĐ</span>
          </div>
          <button 
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
            onClick={() => window.location.href = '/checkout'}
          >
            Thanh toán
          </button>
        </div>
      </div>
    </div>
  );
};

export default CartComponent;
import React from "react";
import { useState, useEffect } from "react";

const ShoppingCart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [total, setTotal] = useState(0);

  const updateItemQuantity = async (productId, action) => {
    try {
      const response = await fetch("/update-item/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          productId: productId,
          action: action,
        }),
      });

      if (response.ok) {
        location.reload();
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Giỏ hàng của bạn</h2>
          <span className="text-gray-600">({cartItems.length} sản phẩm)</span>
        </div>

        <div className="divide-y divide-gray-200">
          {cartItems.map((item) => (
            <div
              key={item.id}
              className="py-4 flex justify-between items-center"
            >
              <div className="flex items-center space-x-4">
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-20 h-20 object-cover rounded"
                />
                <div>
                  <h3 className="font-medium">{item.name}</h3>
                  <p className="text-gray-500">
                    {item.price.toLocaleString()} VNĐ
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <div className="flex items-center border rounded">
                  <button
                    onClick={() => updateItemQuantity(item.id, "remove")}
                    className="px-3 py-1 hover:bg-gray-100"
                  >
                    -
                  </button>
                  <span className="px-3 py-1">{item.quantity}</span>
                  <button
                    onClick={() => updateItemQuantity(item.id, "add")}
                    className="px-3 py-1 hover:bg-gray-100"
                  >
                    +
                  </button>
                </div>
                <span className="font-medium">
                  {(item.price * item.quantity).toLocaleString()} VNĐ
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 pt-6 border-t">
          <div className="flex justify-between text-xl font-bold">
            <span>Tổng cộng:</span>
            <span>{total.toLocaleString()} VNĐ</span>
          </div>
          <button
            onClick={() => (window.location.href = "/checkout")}
            className="mt-4 w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700"
          >
            Tiến hành thanh toán
          </button>
        </div>
      </div>
    </div>
  );
};

export default ShoppingCart;

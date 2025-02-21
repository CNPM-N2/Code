document.addEventListener('DOMContentLoaded', function() {
    const showToast = (message, type = 'success') => {
        const toast = document.getElementById('toast');
        if (!toast) return;
        
        toast.textContent = message;
        toast.className = `toast ${type} show`;
        
        setTimeout(() => {
            toast.className = 'toast';
        }, 3000);
    };

    const handleQuantityUpdate = async (productId, action) => {
        if (user === 'AnonymousUser') {
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
                    'productId': productId,
                    'action': action
                })
            });

            const data = await response.json();
            
            if (data.status === 'success') {
                const row = document.querySelector(`tr[data-product-id="${productId}"]`);
                if (row) {
                    const quantityInput = row.querySelector('.quantity-input');
                    const currentQuantity = parseInt(quantityInput.value);
                    
                    if (action === 'add') {
                        quantityInput.value = currentQuantity + 1;
                    } else if (action === 'remove') {
                        if (currentQuantity > 1) {
                            quantityInput.value = currentQuantity - 1;
                        } else {
                            row.remove();
                        }
                    }

                    const priceElement = row.querySelector('.price');
                    if (priceElement && data.itemTotal) {
                        priceElement.textContent = `${parseFloat(data.itemTotal).toLocaleString()} VND`;
                    }

                    const totalElement = document.querySelector('.total-row .price');
                    if (totalElement && data.cartTotal) {
                        totalElement.textContent = `${parseFloat(data.cartTotal).toLocaleString()} VND`;
                    }
                }

                showToast('Cập nhật giỏ hàng thành công!');
            } else {
                showToast('Có lỗi xảy ra khi cập nhật giỏ hàng', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('Có lỗi xảy ra khi cập nhật giỏ hàng', 'error');
        }
    };

    const quantityButtons = document.querySelectorAll('.quantity-btn');
    quantityButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.closest('tr').dataset.productId;
            const action = this.dataset.action;
            handleQuantityUpdate(productId, action);
        });
    });

    function getCookie(name) {
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
    }
});
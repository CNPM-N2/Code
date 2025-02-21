// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get all buttons with the update-cart class
    var updateBtns = document.getElementsByClassName('update-cart');
    
    // Add click event listener to each button
    for (i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function(e) {
            e.preventDefault();
            var productId = this.dataset.product;
            var action = this.dataset.action;
            
            console.log('productId:', productId, 'action:', action);
            
            // Check if user is authenticated
            if (user === 'AnonymousUser') {
                console.log('User is not logged in');
                // You could redirect to login page or show a message
                alert('Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng');
            } else {
                updateUserOrder(productId, action);
            }
        });
    }
    
    // Function to update order through AJAX
    function updateUserOrder(productId, action) {
        console.log('Updating cart...');
        
        // Show loading indicator
        const button = document.querySelector(`button[data-product="${productId}"][data-action="${action}"]`);
        const originalText = button.textContent;
        button.textContent = action === 'add' ? '+' : '-';
        button.disabled = true;
        
        // URL to send the request to
        var url = '/update_item/';
        
        // Send AJAX request
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'productId': productId,
                'action': action
            })
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log('Success:', data);
            // Update the page without reloading
            if (data.itemCount !== undefined) {
                // Find the right quantity display
                const quantityDisplay = button.parentElement.querySelector('.quantity-display');
                if (quantityDisplay) {
                    quantityDisplay.textContent = data.itemCount;
                }
                
                // Update the total at the top
                const totalElement = document.querySelector('h5:contains("Tổng thanh toán")');
                if (totalElement && data.cartTotal !== undefined) {
                    totalElement.innerHTML = `Tổng thanh toán: <strong>${data.cartTotal} VND</strong>`;
                }
                
                // Update item total for this row
                const rowTotal = button.closest('.cart-row').querySelector('div:last-child p');
                if (rowTotal && data.itemTotal !== undefined) {
                    rowTotal.textContent = `${data.itemTotal} VND`;
                }
                
                // If quantity is zero, consider removing the row
                if (data.itemCount === 0) {
                    button.closest('.cart-row').remove();
                }
            } else {
                // If no specific data returned, reload the page
                location.reload();
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi cập nhật giỏ hàng');
        })
        .finally(() => {
            // Re-enable button
            button.textContent = originalText;
            button.disabled = false;
        });
    }
    
    // Add visual feedback when clicking checkout button
    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function(e) {
            // Only add visual effect if there are items in the cart
            const cartItems = document.querySelector('h5:contains("Mặt hàng")');
            if (cartItems && cartItems.textContent.includes('0')) {
                e.preventDefault();
                alert('Giỏ hàng của bạn đang trống');
            } else {
                this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Đang xử lý...';
                // Allow the navigation to continue
            }
        });
    }
});
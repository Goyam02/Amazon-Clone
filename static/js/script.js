// Amazon Clone JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Back to top button functionality
    const backToTopButton = document.querySelector('.back-to-top a');
    if (backToTopButton) {
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Product quantity buttons
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(function(input) {
        const decrementBtn = input.parentElement.querySelector('.decrement-btn');
        const incrementBtn = input.parentElement.querySelector('.increment-btn');

        if (decrementBtn) {
            decrementBtn.addEventListener('click', function() {
                const currentValue = parseInt(input.value);
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                }
            });
        }

        if (incrementBtn) {
            incrementBtn.addEventListener('click', function() {
                const currentValue = parseInt(input.value);
                const maxValue = parseInt(input.getAttribute('max') || 99);
                if (currentValue < maxValue) {
                    input.value = currentValue + 1;
                }
            });
        }
    });

    // Product image zoom effect on hover
    const productImages = document.querySelectorAll('.product-detail-image');
    productImages.forEach(function(img) {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.3s';
        });

        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Payment method toggle (show/hide credit card fields)
    const paymentMethodSelect = document.querySelector('#payment_method');
    const cardFields = document.querySelector('.card-fields');

    if (paymentMethodSelect && cardFields) {
        // Initially hide card fields if payment method is not 'card'
        if (paymentMethodSelect.value !== 'card') {
            cardFields.style.display = 'none';
        }

        paymentMethodSelect.addEventListener('change', function() {
            if (this.value === 'card') {
                cardFields.style.display = 'block';
            } else {
                cardFields.style.display = 'none';
            }
        });
    }

    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000); // Auto-dismiss after 5 seconds
    });
});

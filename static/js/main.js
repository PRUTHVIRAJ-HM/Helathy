/**
 * Food Safety Advisor - Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // File upload validation and preview
    const prescriptionInput = document.getElementById('prescription');
    if (prescriptionInput) {
        prescriptionInput.addEventListener('change', function() {
            validateFileUpload(this);
        });
    }
    
    // Form validation
    const form = document.getElementById('food-safety-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                return false;
            }
            showLoadingState();
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

/**
 * Validates the uploaded file type
 * @param {HTMLInputElement} fileInput - The file input element
 * @returns {boolean} - Whether the file is valid
 */
function validateFileUpload(fileInput) {
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (fileInput.files.length === 0) {
        return false;
    }
    
    const file = fileInput.files[0];
    
    // Check file type
    if (!allowedTypes.includes(file.type)) {
        alert('Please upload a valid file type (PDF, JPG, or PNG)');
        fileInput.value = '';
        return false;
    }
    
    // Check file size
    if (file.size > maxSize) {
        alert('File size exceeds maximum limit of 16MB');
        fileInput.value = '';
        return false;
    }
    
    return true;
}

/**
 * Validates the entire form before submission
 * @returns {boolean} - Whether the form is valid
 */
function validateForm() {
    const foodProduct = document.getElementById('food_product');
    const prescription = document.getElementById('prescription');
    
    if (!foodProduct || !prescription) {
        return true; // Elements don't exist, let the form submit
    }
    
    // Validate food product field
    if (!foodProduct.value.trim()) {
        alert('Please enter a food product name');
        foodProduct.focus();
        return false;
    }
    
    // Validate prescription file
    if (prescription.files.length === 0) {
        alert('Please upload your prescription');
        prescription.focus();
        return false;
    }
    
    return validateFileUpload(prescription);
}

/**
 * Shows loading state on form submission
 */
function showLoadingState() {
    const button = document.getElementById('analyze-btn');
    if (button) {
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Analyzing...';
        button.disabled = true;
        
        // Apply pulsating effect to the card
        const card = button.closest('.card');
        if (card) {
            card.classList.add('pulsate');
        }
    }
}

/**
 * Cycles through images in the carousel
 */
function initImageCarousel() {
    const images = [
        'https://pixabay.com/get/gaa81587e96361bafa2d0ce941858b0cb33c25d50c468d956fdef42bb7dfcbda28dd8ffa8929f4c9d0242424dcc7bf6ade90e9a4b43f36524912ca8243c9ec00c_1280.jpg',
        'https://pixabay.com/get/g444e8a2fb213dd667f221cf3d8e8dd7046ca184d2368ff030deb748193b0b7e5e8d98aa0c295d0bf886e7fe8aaaab04395331b53d2aeeeff922ceef6373f8ad5_1280.jpg',
        'https://pixabay.com/get/g1d42e670ffb1226070b5c3079dca1dae368b97773d205daf5a143906b54b884b879dd2d9e846e2e2a9a63703a0e4c27f7b5051d5b0c56225dadf718a4373abc8_1280.jpg',
        'https://pixabay.com/get/g06a875eac051495ee42bfed6c9b324c46aeec6aeb2ff6ea050d50234de474a66c61a2f92e2a81fd712699834eec52063e94e3988bcd07f6fc0cff377f826cad2_1280.jpg',
        'https://pixabay.com/get/gbccb8b4f5dea2ea080b1d3d2946b18d1ae118f4f4f1452d50ed4c93e0d28645488dceb390a9b93932a9b21932139c3dc74195f0f109d6057bf31a30b9506809d_1280.jpg'
    ];
    
    const carouselElement = document.querySelector('.carousel-images img');
    if (!carouselElement) return;
    
    let currentIndex = 0;
    
    // Change image every 5 seconds
    setInterval(() => {
        currentIndex = (currentIndex + 1) % images.length;
        
        // Fade out current image
        carouselElement.style.opacity = 0;
        
        // After fade out, change source and fade in
        setTimeout(() => {
            carouselElement.src = images[currentIndex];
            carouselElement.style.opacity = 1;
        }, 500);
    }, 5000);
}

// Initialize carousel if images are available
if (document.querySelector('.carousel-images')) {
    initImageCarousel();
}

/**
 * Student Freelance Marketplace - JavaScript Interactivity
 * Beginner-friendly vanilla JavaScript for:
 * 1. Password visibility toggle
 * 2. Confirmation alerts for critical actions (Delete project, Accept proposal)
 * 3. Client-side form validation feedback
 * 4. Automatic dismissal of alert notices
 */

document.addEventListener('DOMContentLoaded', function () {
    
    // -------------------------------------------------------------------------
    // 1. Password Visibility Toggle (Show / Hide Password)
    // -------------------------------------------------------------------------
    const togglePasswordBtns = document.querySelectorAll('.toggle-password-btn');
    
    togglePasswordBtns.forEach(function (button) {
        button.addEventListener('click', function () {
            const targetInputId = button.getAttribute('data-target');
            const passwordInput = document.getElementById(targetInputId);
            
            if (passwordInput) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    button.innerHTML = '<i class="bi bi-eye-slash"></i> Hide';
                } else {
                    passwordInput.type = 'password';
                    button.innerHTML = '<i class="bi bi-eye"></i> Show';
                }
            }
        });
    });

    // -------------------------------------------------------------------------
    // 2. Confirmation Prompt for Project Deletion
    // -------------------------------------------------------------------------
    const deleteButtons = document.querySelectorAll('.btn-confirm-delete');
    
    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            const projectTitle = button.getAttribute('data-title') || 'this project';
            const confirmed = window.confirm(
                `Are you sure you want to delete "${projectTitle}"?\nThis action cannot be undone.`
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // -------------------------------------------------------------------------
    // 3. Confirmation Prompt for Accepting a Proposal
    // -------------------------------------------------------------------------
    const acceptButtons = document.querySelectorAll('.btn-confirm-accept');
    
    acceptButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            const studentName = button.getAttribute('data-student') || 'this student';
            const confirmed = window.confirm(
                `Are you sure you want to accept the proposal from ${studentName}?\nThis will mark the project as Assigned and reject other proposals.`
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // -------------------------------------------------------------------------
    // 4. Auto-dismiss alerts after 5 seconds
    // -------------------------------------------------------------------------
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Use Bootstrap's alert close if available, else fade out
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 5000);
    });

    // -------------------------------------------------------------------------
    // 5. Basic Frontend Validation for Numbers (Budget & Days)
    // -------------------------------------------------------------------------
    const positiveInputs = document.querySelectorAll('input[type="number"][min="1"]');
    positiveInputs.forEach(function (input) {
        input.addEventListener('change', function () {
            if (parseFloat(input.value) <= 0) {
                alert('Value must be greater than zero.');
                input.value = '';
                input.focus();
            }
        });
    });

});


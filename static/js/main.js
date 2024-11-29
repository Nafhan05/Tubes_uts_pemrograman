// main.js

// Toggle Password Visibility
function togglePassword(passwordId, iconId) {
    const passwordInput = document.getElementById(passwordId);
    const icon = document.getElementById(iconId);

    if (passwordInput && icon) {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
        } else {
            passwordInput.type = "password";
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
        }
    }
}

// Toggle Settings Dropdown
function toggleSettingsDropdown() {
    const settingsDropdown = document.getElementById('settingsDropdown');
    const settingsIcon = document.getElementById('settingsIcon');

    if (settingsDropdown && settingsIcon) {
        // Check if dropdown is visible
        if (settingsDropdown.style.display === "block") {
            // Hide dropdown with reverse animation
            settingsDropdown.style.opacity = "0";
            settingsDropdown.style.transform = "scaleY(0)";
            setTimeout(() => {
                settingsDropdown.style.display = "none";
            }, 300); // Delay to match the CSS transition duration
            settingsIcon.style.transform = "rotate(0deg)"; // Rotate back on hide
        } else {
            // Show dropdown with animation
            settingsDropdown.style.display = "block";
            setTimeout(() => {
                settingsDropdown.style.opacity = "1";
                settingsDropdown.style.transform = "scaleY(1)";
                settingsIcon.style.transform = "rotate(90deg)"; // Rotate on show
            }, 10); // Slight delay to trigger transition
        }
    }
}


// Dropdown Menu Interaction for Reservation
function toggleReservationDropdown() {
    const reservationDropdown = document.getElementById('reservationDropdown');
    const reservationButton = document.getElementById('reservationButton');
    const reservationIcon = document.getElementById('reservationIcon');

    // Toggle dropdown visibility on click (stay open if clicked)
    reservationButton.addEventListener('click', function () {
        if (reservationDropdown.classList.contains('show')) {
            // Hide dropdown if already open
            hideDropdown(reservationDropdown);
            reservationIcon.textContent = "▼"; // Change back to down arrow
        } else {
            // Show dropdown if closed
            showDropdown(reservationDropdown);
            reservationIcon.textContent = "▲"; // Change to up arrow when open
        }
    });

    // Show dropdown with animation
    function showDropdown(dropdown) {
        dropdown.style.display = "block";
        setTimeout(() => {
            dropdown.classList.add('show');  // Add the 'show' class to trigger the animation
            dropdown.style.opacity = "1";
            dropdown.style.transform = "scaleY(1)";
        }, 10);
    }

    // Hide dropdown with animation
    function hideDropdown(dropdown) {
        dropdown.style.opacity = "0";
        dropdown.style.transform = "scaleY(0)";
        setTimeout(() => {
            dropdown.classList.remove('show');  // Remove the 'show' class to hide the dropdown
            dropdown.style.display = "none";
        }, 300);
    }
}




document.addEventListener('DOMContentLoaded', function () {

    // Settings Button Listener
    const settingsButton = document.getElementById('settingsButton');
    if (settingsButton) {
        settingsButton.addEventListener('click', function () {
            toggleSettingsDropdown();
        });
    }

    // Reservation Button Listener
    const reservationButton = document.getElementById('reservationButton');
    if (reservationButton) {
        toggleReservationDropdown();  // Initialize dropdown for reservation
    }

    // Form Validation for Login and Register
    const loginForm = document.querySelector('#loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            const username = document.querySelector('[name="username"]').value.trim();
            const password = document.querySelector('[name="password"]').value.trim();

            if (username === '' || password === '') {
                e.preventDefault();
                alert('Please fill out all fields');
            }
        });
    }

    const registerForm = document.querySelector('#registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            const username = document.querySelector('[name="username"]').value.trim();
            const password = document.querySelector('[name="password"]').value.trim();
            const confirmPassword = document.querySelector('[name="confirm_password"]').value.trim();

            if (username === '' || password === '' || confirmPassword === '') {
                e.preventDefault();
                alert('Please fill out all fields');
            } else if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match');
            }
        });
    }

    // Toggle Sidebar for Mobile View
    const toggleButton = document.querySelector('#toggleSidebar');
    const sidebar = document.querySelector('#sidebar');

    if (toggleButton && sidebar) {
        toggleButton.addEventListener('click', () => {
            sidebar.classList.toggle('hidden');
        });
    }

    const checkbox = document.getElementById('change-credentials-checkbox');
    const changeCredentialsForm = document.getElementById('change-credentials-form');

    // Tampilkan atau sembunyikan form ganti username/password berdasarkan checkbox
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            changeCredentialsForm.classList.remove('hidden');
        } else {
            changeCredentialsForm.classList.add('hidden');
        }
    });
    
});

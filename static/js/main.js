// main.js

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
    const reservationIcon = document.getElementById('reservationIcon');

    if (reservationDropdown && reservationIcon) {
        // Check if dropdown is visible
        if (reservationDropdown.style.display === "block") {
            // Hide dropdown with reverse animation
            reservationDropdown.style.opacity = "0";
            reservationDropdown.style.transform = "scaleY(0)";
            setTimeout(() => {
                reservationDropdown.style.display = "none";
                reservationIcon.textContent = "▼"; // Change back to down arrow
            }, 300); // Delay to match the CSS transition duration
        } else {
            // Show dropdown with animation
            reservationDropdown.style.display = "block";
            setTimeout(() => {
                reservationDropdown.style.opacity = "1";
                reservationDropdown.style.transform = "scaleY(1)";
                // reservationIcon.textContent = "🔼"; // Change to up arrow when open
            }, 10); // Slight delay to trigger transition
        }
    }
}



document.addEventListener('DOMContentLoaded', function () {

    const settingsButton = document.getElementById('settingsButton');
    if (settingsButton) {
        settingsButton.addEventListener('click', function () {
            toggleSettingsDropdown();
        });
    }

    const reservationButton = document.getElementById('reservationButton');
    if (reservationButton) {
        reservationButton.addEventListener('click', function () {
            toggleReservationDropdown();
        });
    }
    
    // Fungsi validasi form login
    const loginForm = document.querySelector('#loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            // Contoh validasi sederhana sebelum form dikirimkan
            const username = document.querySelector('[name="username"]').value.trim();
            const password = document.querySelector('[name="password"]').value.trim();

            if (username === '' || password === '') {
                e.preventDefault(); // Mencegah pengiriman form
                alert('Please fill out all fields');
            }
        });
    }

    // Fungsi validasi form registrasi
    const registerForm = document.querySelector('#registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            // Contoh validasi sederhana sebelum form dikirimkan
            const username = document.querySelector('[name="username"]').value.trim();
            const password = document.querySelector('[name="password"]').value.trim();
            const confirmPassword = document.querySelector('[name="confirm_password"]').value.trim();

            if (username === '' || password === '' || confirmPassword === '') {
                e.preventDefault(); // Mencegah pengiriman form
                alert('Please fill out all fields');
            } else if (password !== confirmPassword) {
                e.preventDefault(); // Mencegah pengiriman form
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

    // Event listener untuk semua tombol (contoh interaksi sederhana)
    const submitButtons = document.querySelectorAll('.btn');
    submitButtons.forEach(button => {
        button.addEventListener('click', function () {
            console.log('Button clicked:', button);
        });
    });
});

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

// Menampilkan notifikasi sukses
function showSuccessNotification(message) {
    const successNotification = document.getElementById('success-notification');
    successNotification.innerText = message;
    successNotification.classList.remove('hidden');
    setTimeout(() => {
        successNotification.classList.add('hidden');
    }, 3000);
}


// Fungsi untuk menginisialisasi flatpickr pada elemen tanggal
function initDatepicker() {
    flatpickr("#reservationDate", {
        enableTime: false,
        dateFormat: "Y-m-d",
        minDate: "today",
    });
}

// Fungsi untuk menginisialisasi flatpickr pada elemen bulan
function initMonthpicker() {
    flatpickr("#reservationMonth", {
        enableTime: false,
        dateFormat: "F Y",
        monthSelectorType: "static",
    });
}

// Fungsi utama untuk menginisialisasi semua pengaturan flatpickr
function initializePickers() {
    initDatepicker();
    initMonthpicker();
}


function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notification-message');

    // Ubah pesan dan warna berdasarkan tipe
    notificationMessage.textContent = message;
    notification.className = `fixed top-5 right-5 py-2 px-4 rounded shadow ${type === 'success' ? 'bg-blue-600' : 'bg-red-600'} show`;

    // Sembunyikan notifikasi setelah beberapa detik
    setTimeout(() => {
        notification.className = 'hidden';
    }, 3000);
}


document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('personalDataForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            const fullName = document.getElementById('full_name').value;
            const nik = document.getElementById('nik').value;
            const domicile = document.getElementById('domicile').value;
            const phone = document.getElementById('phone').value;

            // Validate form fields
            if (!fullName || !nik || !domicile || !phone) {
                e.preventDefault();
                alert('Please fill out all fields.');
            }
        })
    }

    // Settings Button Listener
    const settingsButton = document.getElementById('settingsButton');
    if (settingsButton) {
        settingsButton.addEventListener('click', function () {
            toggleSettingsDropdown();
        })
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
        })
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
        })
    }

    // Toggle Sidebar for Mobile View
    const toggleButton = document.querySelector('#toggleSidebar');
    const sidebar = document.querySelector('#sidebar');

    if (toggleButton && sidebar) {
        toggleButton.addEventListener('click', () => {
            sidebar.classList.toggle('hidden');
        })
    }

    this.form.submit(); // Submit form untuk memperbarui waktu secara otomatis
    initializePickers();
    
});


// Event listener untuk form submit
document.getElementById('personalDataForm').addEventListener('submit', function (e) {
    if (validateForm()) {
        // Jika validasi berhasil, hapus preventDefault agar form terkirim
        e.preventDefault(); // Hapus jika validasi berhasil
        this.submit(); // Kirim form
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    
    if (chatForm) {
        chatForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            
            const messageInput = this.querySelector('input[name="message"]');
            const message = messageInput.value.trim();
            const patientId = window.patientId;  // Ambil dari template

            if (message) {
                try {
                    const response = await fetch(`/chat_admin/${patientId}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message })
                    });

                    const data = await response.json();

                    if (data.success) {
                        const chatMessages = document.getElementById('chat-messages');
                        const newMessage = `
                            <div class="message-chat sent-admin" data-message-id="${data.id}">
                                <p>${data.message}</p>
                                <small>${data.timestamp}</small><br>
                                <span class="read-status">Sent</span>
                            </div>
                        `;

                        if (chatMessages) {
                            chatMessages.innerHTML += newMessage;
                            messageInput.value = '';  // Kosongkan input setelah kirim
                            chatMessages.scrollTop = chatMessages.scrollHeight;  // Auto-scroll
                        }
                    } else {
                        alert('Failed to send message.');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('An error occurred while sending the message.');
                }
            }
        });
    } else {
        console.error("Chat form not found.");
    }
});




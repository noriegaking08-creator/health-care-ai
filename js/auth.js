// auth.js - Authentication functionality
document.addEventListener('DOMContentLoaded', async function() {
    // Wait for API to initialize
    await window.HealthComAPI.initializeAPI().then(service => {
        window.APIService = service;
    });

    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const loginMessage = document.getElementById('loginMessage');
    const registerMessage = document.getElementById('registerMessage');

    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const username = document.getElementById('loginUsername').value.trim();
            const password = document.getElementById('loginPassword').value;

            if (!username || !password) {
                showMessage(loginMessage, 'Please fill in all fields', 'error');
                return;
            }

            try {
                const response = await window.APIService.login({ username, password });
                window.SessionManager.setUser({ id: response.user_id, username });

                showMessage(loginMessage, 'Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = 'chat.html';
                }, 1500);
            } catch (error) {
                showMessage(loginMessage, error.message, 'error');
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            const fullName = document.getElementById('fullName').value.trim();
            const age = document.getElementById('age').value;
            const location = document.getElementById('location').value.trim();

            if (!username || !password) {
                showMessage(registerMessage, 'Username and password are required', 'error');
                return;
            }

            if (password.length < 6) {
                showMessage(registerMessage, 'Password must be at least 6 characters', 'error');
                return;
            }

            const userData = {
                username,
                password,
                full_name: fullName,
                age: age ? parseInt(age) : null,
                location: location || 'Malawi'
            };

            try {
                const response = await window.APIService.register(userData);
                showMessage(registerMessage, 'Registration successful! Please login.', 'success');

                // Clear form
                registerForm.reset();
                document.getElementById('location').value = 'Malawi';

                // Redirect to login after delay
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 2000);
            } catch (error) {
                showMessage(registerMessage, error.message, 'error');
            }
        });
    }

    function showMessage(element, message, type) {
        element.textContent = message;
        element.className = `message ${type} show`;

        // Auto-hide success messages after 3 seconds
        if (type === 'success') {
            setTimeout(() => {
                element.classList.remove('show');
            }, 3000);
        }
    }
});
// main.js - Main application functionality
document.addEventListener('DOMContentLoaded', async function() {
    // Wait for API to initialize
    await window.HealthComAPI.initializeAPI().then(service => {
        window.APIService = service;
    });

    // Navigation functionality
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Update navigation based on authentication
    updateNavBasedOnAuth();

    // Logout functionality
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.SessionManager.clearUser();
            window.location.href = 'index.html';
        });
    }

    // Profile page functionality
    loadUserProfile();
});

function updateNavBasedOnAuth() {
    const isAuthenticated = window.SessionManager.isAuthenticated();
    const navMenu = document.querySelector('.nav-menu');

    if (!navMenu) return;

    // Clear existing nav items
    navMenu.innerHTML = '';

    // Add basic nav items
    const homeLink = createNavLink('index.html', 'Home');
    navMenu.appendChild(homeLink);

    if (isAuthenticated) {
        // Add authenticated nav items
        const chatLink = createNavLink('chat.html', 'Chat');
        const profileLink = createNavLink('profile.html', 'Profile');
        const logoutLink = document.createElement('li');
        logoutLink.innerHTML = '<a href="#" class="nav-link" id="logoutBtn">Logout</a>';

        navMenu.appendChild(chatLink);
        navMenu.appendChild(profileLink);
        navMenu.appendChild(logoutLink);

        // Add logout event listener
        document.getElementById('logoutBtn').addEventListener('click', function(e) {
            e.preventDefault();
            window.SessionManager.clearUser();
            window.location.href = 'index.html';
        });
    } else {
        // Add unauthenticated nav items
        const loginLink = createNavLink('login.html', 'Login');
        const registerLink = createNavLink('register.html', 'Register');

        navMenu.appendChild(loginLink);
        navMenu.appendChild(registerLink);
    }
}

function createNavLink(href, text) {
    const li = document.createElement('li');
    const link = document.createElement('a');
    link.href = href;
    link.className = 'nav-link';
    link.textContent = text;

    // Set active class if current page
    if (window.location.pathname.includes(href.replace('.html', ''))) {
        link.classList.add('active');
    }

    li.appendChild(link);
    return li;
}

async function loadUserProfile() {
    const profilePage = document.querySelector('.profile-container');
    if (!profilePage) return;

    // Check authentication
    window.SessionManager.redirectIfNotAuthenticated();

    const user = window.SessionManager.getUser();
    if (!user) return;

    try {
        const profile = await window.APIService.getUserProfile(user.id);

        // Update profile information
        document.getElementById('profileName').textContent = profile.full_name || profile.username;
        document.getElementById('profileUsername').textContent = `@${profile.username}`;
        document.getElementById('profileFullName').textContent = profile.full_name || '-';
        document.getElementById('profileAge').textContent = profile.age || '-';
        document.getElementById('profileLocation').textContent = profile.location || '-';
    } catch (error) {
        console.error('Error loading profile:', error);
        // Show error message to user
    }
}

// Utility function to show toast messages
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: var(--${type === 'error' ? 'danger' : type === 'success' ? 'secondary' : 'primary'}-color);
        color: white;
        border-radius: 5px;
        z-index: 1000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;

    document.body.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 100);

    // Remove after delay
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Add smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    }
});

// Form validation utilities
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

// Export utilities for other modules
window.HealthComUtils = {
    showToast,
    validateEmail,
    validatePassword
};
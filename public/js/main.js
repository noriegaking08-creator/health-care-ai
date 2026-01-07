// main.js - Enhanced application functionality with animations and personalization
document.addEventListener('DOMContentLoaded', async function() {
    // Show welcome animation
    showWelcomeAnimation();

    // Wait for API to initialize
    await window.HealthComAPI.initializeAPI().then(service => {
        window.APIService = service;
    });

    // Initialize enhanced features
    initializeEnhancedFeatures();

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
            showAnimatedRedirect('index.html', 'You have been logged out successfully!');
        });
    }

    // Profile page functionality
    loadUserProfile();

    // Initialize page-specific enhancements
    initializePageSpecificFeatures();
});

function showWelcomeAnimation() {
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'welcome-animation';
    welcomeDiv.innerHTML = `
        <div class="welcome-content">
            <h1><i class="fas fa-heartbeat"></i> HealthCare AI</h1>
            <p>Your Personal Health Companion</p>
        </div>
    `;
    document.body.appendChild(welcomeDiv);

    setTimeout(() => {
        welcomeDiv.style.animation = 'welcomeFadeOut 1s ease-in-out forwards';
        setTimeout(() => {
            document.body.removeChild(welcomeDiv);
        }, 1000);
    }, 2500);
}

function initializeEnhancedFeatures() {
    // Add floating animation to hero section elements
    animateHeroElements();

    // Initialize scroll animations
    initializeScrollAnimations();

    // Add typing effects to text elements
    initializeTypingEffects();

    // Add interactive hover effects
    addInteractiveEffects();
}

function animateHeroElements() {
    const heroElements = document.querySelectorAll('.hero-content h1, .hero-content p, .hero-buttons .btn');
    heroElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';

        setTimeout(() => {
            element.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 300 + (index * 200));
    });
}

function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        observer.observe(card);
    });
}

function initializeTypingEffects() {
    const typingElements = document.querySelectorAll('[data-typing]');
    typingElements.forEach(element => {
        const text = element.getAttribute('data-typing');
        typeText(element, text);
    });
}

function typeText(element, text) {
    let i = 0;
    element.textContent = '';

    function typeWriter() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 50);
        }
    }

    setTimeout(typeWriter, 1000);
}

function addInteractiveEffects() {
    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            createRippleEffect(e, this);
        });
    });

    // Add hover effects to cards
    document.querySelectorAll('.feature-card, .profile-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

function createRippleEffect(e, element) {
    const circle = document.createElement('span');
    const diameter = Math.max(element.clientWidth, element.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${e.clientX - element.getBoundingClientRect().left - radius}px`;
    circle.style.top = `${e.clientY - element.getBoundingClientRect().top - radius}px`;
    circle.classList.add('ripple');

    const ripple = element.getElementsByClassName('ripple')[0];
    if (ripple) {
        ripple.remove();
    }

    element.appendChild(circle);
}

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
            showAnimatedRedirect('index.html', 'You have been logged out successfully!');
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

        // Update profile information with animations
        animateElement('#profileName', profile.full_name || profile.username);
        animateElement('#profileUsername', `@${profile.username}`);
        animateElement('#profileFullName', profile.full_name || '-');
        animateElement('#profileAge', profile.age || '-');
        animateElement('#profileLocation', profile.location || '-');

        // Add personalized greeting
        addPersonalizedGreeting(profile);
    } catch (error) {
        console.error('Error loading profile:', error);
        showToast('Failed to load profile information', 'error');
    }
}

function animateElement(selector, text) {
    const element = document.querySelector(selector);
    if (element) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(10px)';

        setTimeout(() => {
            element.textContent = text;
            element.style.transition = 'all 0.5s ease-out';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100);
    }
}

function addPersonalizedGreeting(profile) {
    const greetingElement = document.createElement('div');
    greetingElement.className = 'personalized-greeting';
    greetingElement.innerHTML = `
        <div style="
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 15px;
            text-align: center;
        ">
            Welcome back, ${profile.full_name || profile.username}!
            <i class="fas fa-heart"></i>
        </div>
    `;

    const profileInfo = document.querySelector('.profile-info');
    if (profileInfo) {
        profileInfo.appendChild(greetingElement);
    }
}

function initializePageSpecificFeatures() {
    const currentPage = window.location.pathname.split('/').pop();

    switch(currentPage) {
        case 'index.html':
        case '':
            initializeHomePageFeatures();
            break;
        case 'chat.html':
            initializeChatPageFeatures();
            break;
        case 'profile.html':
            initializeProfilePageFeatures();
            break;
    }
}

function initializeHomePageFeatures() {
    // Add dynamic health tips
    addDynamicHealthTips();

    // Initialize testimonial carousel
    initializeTestimonialCarousel();
}

function addDynamicHealthTips() {
    const tips = [
        "Drink at least 8 glasses of water daily for optimal hydration.",
        "Aim for 7-9 hours of quality sleep each night.",
        "Include fruits and vegetables in every meal.",
        "Take short walks throughout the day to stay active.",
        "Practice deep breathing exercises to reduce stress."
    ];

    const tipElement = document.createElement('div');
    tipElement.className = 'health-tip';
    tipElement.style.cssText = `
        background: rgba(255,255,255,0.9);
        padding: 15px 20px;
        border-radius: var(--border-radius);
        margin: 20px auto;
        max-width: 600px;
        text-align: center;
        font-style: italic;
        color: var(--text-color);
        box-shadow: var(--shadow);
        animation: fadeInUp 0.8s ease;
    `;

    const randomTip = tips[Math.floor(Math.random() * tips.length)];
    tipElement.textContent = `💡 ${randomTip}`;

    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        heroSection.appendChild(tipElement);
    }
}

function initializeTestimonialCarousel() {
    // This would be implemented with actual testimonials
    console.log('Testimonial carousel initialized');
}

function initializeChatPageFeatures() {
    // Add typing indicators
    addTypingIndicators();

    // Initialize chat history animations
    initializeChatHistoryAnimations();
}

function addTypingIndicators() {
    // Add typing indicator functionality
    console.log('Typing indicators added');
}

function initializeChatHistoryAnimations() {
    // Animate existing chat messages
    const messages = document.querySelectorAll('.message');
    messages.forEach((message, index) => {
        message.style.opacity = '0';
        message.style.transform = 'translateY(20px)';

        setTimeout(() => {
            message.style.transition = 'all 0.5s ease-out';
            message.style.opacity = '1';
            message.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

function initializeProfilePageFeatures() {
    // Add profile completion suggestions
    addProfileCompletionSuggestions();
}

function addProfileCompletionSuggestions() {
    // Add suggestions for profile completion
    console.log('Profile completion suggestions added');
}

// Utility function to show toast messages with enhanced styling
function showToast(message, type = 'info') {
    // Remove existing toasts
    document.querySelectorAll('.toast').forEach(toast => toast.remove());

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i> ${message}`;

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
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

// Enhanced redirect with animation
function showAnimatedRedirect(url, message) {
    if (message) {
        showToast(message, 'success');
    }

    setTimeout(() => {
        window.location.href = url;
    }, 1000);
}

// Add smooth scrolling for anchor links with enhanced effects
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            // Add scroll animation
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });

            // Add highlight effect
            target.style.animation = 'pulse 1s ease-in-out';
        }
    }
});

// Enhanced form validation utilities
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

function validateFullName(name) {
    return name && name.trim().length >= 2;
}

function validateAge(age) {
    return age && age >= 1 && age <= 120;
}

// Export utilities for other modules
window.HealthComUtils = {
    showToast,
    validateEmail,
    validatePassword,
    validateFullName,
    validateAge
};

// Add ripple effect CSS dynamically
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }

    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
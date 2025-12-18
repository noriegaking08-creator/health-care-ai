// api.js - API configuration and utility functions
const API_BASE_URL = ''; // For Vercel deployment, using relative paths for API routes

// Store user session in localStorage
class SessionManager {
    static setUser(user) {
        localStorage.setItem('healthcom_user', JSON.stringify(user));
    }

    static getUser() {
        const user = localStorage.getItem('healthcom_user');
        return user ? JSON.parse(user) : null;
    }

    static clearUser() {
        localStorage.removeItem('healthcom_user');
    }

    static isAuthenticated() {
        return !!this.getUser();
    }

    static redirectIfNotAuthenticated() {
        if (!this.isAuthenticated()) {
            window.location.href = '/login.html';
        }
    }
}

// API Service for backend communication
class APIService {
    static async request(endpoint, options = {}) {
        // For Vercel deployment, API routes are under /api/
        const url = `/api${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || data.message || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Authentication methods
    static async register(userData) {
        return this.request('/users/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    static async login(credentials) {
        return this.request('/users/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    }

    static async getUserProfile(userId) {
        return this.request(`/users/${userId}`);
    }

    // Chat methods
    static async sendMessage(message, userId) {
        return this.request('/chat/message', {
            method: 'POST',
            body: JSON.stringify({
                user_id: userId,
                message: message
            })
        });
    }

    // Health check
    static async healthCheck() {
        try {
            const response = await fetch('/api/health');
            return response.ok;
        } catch {
            return false;
        }
    }
}

// Mock API service for development without backend (only if real API is unreachable)
class MockAPIService {
    static users = new Map();
    static conversations = new Map();
    static nextId = 1;

    static async register(userData) {
        const userId = this.nextId++;
        const user = {
            id: userId,
            username: userData.username,
            full_name: userData.full_name || '',
            age: userData.age || null,
            location: userData.location || 'Malawi',
            created_at: new Date().toISOString()
        };

        this.users.set(userId, user);
        return { message: "User registered successfully", user_id: userId };
    }

    static async login(credentials) {
        for (let [userId, user] of this.users) {
            if (user.username === credentials.username) {
                // In a real app, you'd check the password hash
                return { message: "Login successful", user_id: userId };
            }
        }
        throw new Error("Invalid credentials");
    }

    static async getUserProfile(userId) {
        const user = this.users.get(userId);
        if (!user) {
            throw new Error("User not found");
        }
        return user;
    }

    static async sendMessage(message, userId) {
        // Simulate AI response based on keywords
        const lowerMessage = message.toLowerCase();
        let response;

        if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
            response = "Hello! I'm Dr. Alistair Finch. How can I assist you with your health today?";
        } else if (lowerMessage.includes('fever') || lowerMessage.includes('temperature')) {
            response = "Based on your reported symptoms, it sounds like you may have a fever. I recommend staying hydrated, resting, and monitoring your temperature. If your fever is high (above 38.5°C/101.3°F) or persists for more than 2 days, please seek medical attention at a local clinic.";
        } else if (lowerMessage.includes('headache') || lowerMessage.includes('pain')) {
            response = "For headaches, I recommend resting in a quiet, dark room and staying hydrated. Over-the-counter pain relievers like paracetamol can help, but follow package instructions. If the headache is severe, persistent, or accompanied by other serious symptoms, please see a healthcare professional.";
        } else if (lowerMessage.includes('stomach') || lowerMessage.includes('nausea')) {
            response = "For stomach issues, stay hydrated with clean water or oral rehydration solutions. Eat light, plain foods like rice, toast, or bananas. Avoid fatty, spicy, or dairy foods. If vomiting or diarrhea persists for more than 24 hours or you show signs of dehydration, seek immediate medical care.";
        } else if (lowerMessage.includes('cough') || lowerMessage.includes('cold')) {
            response = "For coughs and colds, rest well and drink plenty of fluids. Gargling with warm salt water can soothe a sore throat. If you have difficulty breathing, chest pain, or symptoms worsen, please consult with a healthcare provider.";
        } else {
            response = "Thank you for sharing your health concern. I recommend consulting with a healthcare professional for proper evaluation and treatment. I can provide general health guidance, but remember that I'm not a substitute for proper medical diagnosis and treatment.";
        }

        // Store conversation
        if (!this.conversations.has(userId)) {
            this.conversations.set(userId, []);
        }
        this.conversations.get(userId).push({
            user_message: message,
            doctor_response: response,
            timestamp: new Date().toISOString()
        });

        return { response: response };
    }
}

// Check API availability and use appropriate service
async function initializeAPI() {
    const isBackendAvailable = await APIService.healthCheck();
    return isBackendAvailable ? APIService : MockAPIService;
}

// Initialize the API service
let apiService;
initializeAPI().then(service => {
    apiService = service;
    window.APIService = apiService;
});

// Also provide direct access to SessionManager
window.SessionManager = SessionManager;

// Export for use in other files
window.HealthComAPI = {
    APIService: APIService, // Will be updated when API is initialized
    SessionManager: SessionManager,
    initializeAPI: initializeAPI
};
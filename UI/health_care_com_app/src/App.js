import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import ChatInterface from './pages/ChatInterface';
import Login from './pages/Login';
import Register from './pages/Register';
import UserProfile from './pages/UserProfile'; // Placeholder
import Notifications from './pages/Notifications'; // Placeholder
import NewsFeed from './pages/NewsFeed'; // Placeholder
import './styles/global.css';

const App = () => {
    // State to manage user authentication
    const [userId, setUserId] = useState(null);
    const isLoggedIn = !!userId;

    // Simulate session persistence
    useEffect(() => {
        const storedUserId = localStorage.getItem('user_id');
        if (storedUserId) {
            setUserId(parseInt(storedUserId));
        }
    }, []);

    const handleLogin = (id) => {
        setUserId(id);
        localStorage.setItem('user_id', id);
    };

    const handleLogout = () => {
        setUserId(null);
        localStorage.removeItem('user_id');
    };

    return (
        <Router>
            <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
                <Header isLoggedIn={isLoggedIn} onLogout={handleLogout} />
                <main style={{ flexGrow: 1 }}>
                    <Routes>
                        <Route path="/login" element={<Login onLogin={handleLogin} />} />
                        <Route path="/register" element={<Register />} />
                        <Route 
                            path="/" 
                            element={isLoggedIn ? <ChatInterface userId={userId} isLoggedIn={isLoggedIn} /> : <Navigate to="/login" />} 
                        />
                        <Route 
                            path="/profile" 
                            element={isLoggedIn ? <UserProfile userId={userId} /> : <Navigate to="/login" />} 
                        />
                        <Route 
                            path="/notifications" 
                            element={isLoggedIn ? <Notifications userId={userId} /> : <Navigate to="/login" />} 
                        />
                        <Route 
                            path="/news" 
                            element={isLoggedIn ? <NewsFeed /> : <Navigate to="/login" />} 
                        />
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
};

export default App;
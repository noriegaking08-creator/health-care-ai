import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await fetch('http://localhost:8000/users/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Login failed. Check credentials.');
            }

            // Successfully logged in
            onLogin(data.user_id);
            navigate('/');
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="page-container">
            <div style={authContainerStyle}>
                <h2>Welcome Back, Patient</h2>
                <form onSubmit={handleSubmit} style={formStyle}>
                    <input
                        type="text"
                        className="input-field"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <input
                        type="password"
                        className="input-field"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button type="submit" className="primary-btn" style={{ width: '100%', marginTop: '10px' }}>
                        Login Securely
                    </button>
                    {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
                    <p style={{ textAlign: 'center', marginTop: '20px' }}>
                        Don't have an account? <Link to="/register" style={{ color: '#007bff' }}>Register Here</Link> {/* --color-primary */}
                    </p>
                    {/* Note: Password recovery logic would be a separate, more complex component */}
                </form>
            </div>
        </div>
    );
};

const authContainerStyle = {
    width: '100%',      /* Use full available width */
    maxWidth: '100%',   /* Remove any width constraints */
    margin: '20px 0',   /* Remove horizontal auto margin to allow full width */
    padding: '40px',
    backgroundColor: 'white',
    borderRadius: '10px',
    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.05)', // --color-shadow
    textAlign: 'center',
};

const formStyle = {
    marginTop: '20px',
};

export default Login;
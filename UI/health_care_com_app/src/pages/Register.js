import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '', password: '', full_name: '', age: '', location: 'Malawi'
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            const response = await fetch('http://localhost:8000/users/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Registration failed.');
            }

            setSuccess('Registration successful! Redirecting to login...');
            setTimeout(() => navigate('/login'), 2000);
            
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="page-container">
            <div style={authContainerStyle}>
                <h2>Create Your Patient Profile</h2>
                <form onSubmit={handleSubmit} style={formStyle}>
                    <input type="text" className="input-field" name="username" placeholder="Username" onChange={handleChange} required />
                    <input type="password" className="input-field" name="password" placeholder="Password" onChange={handleChange} required />
                    <input type="text" className="input-field" name="full_name" placeholder="Full Name" onChange={handleChange} />
                    <input type="number" className="input-field" name="age" placeholder="Age (e.g., 35)" onChange={handleChange} />
                    <input type="text" className="input-field" name="location" placeholder="Location (e.g., Lilongwe)" value={formData.location} onChange={handleChange} />

                    <button type="submit" className="primary-btn" style={{ width: '100%', marginTop: '10px' }}>
                        Register for Virtual Care
                    </button>
                    {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
                    {success && <p style={{ color: '#28a745', marginTop: '10px' }}>{success}</p>} {/* --color-secondary */}
                    <p style={{ textAlign: 'center', marginTop: '20px' }}>
                        Already registered? <Link to="/login" style={{ color: '#007bff' }}>Login</Link> {/* --color-primary */}
                    </p>
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

export default Register;
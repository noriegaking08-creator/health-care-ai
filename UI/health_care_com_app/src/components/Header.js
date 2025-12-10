import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Header = ({ isLoggedIn, onLogout }) => {
    const navigate = useNavigate();
    const notificationCount = 3; // Placeholder for actual count
    const [isLogoutHovered, setIsLogoutHovered] = useState(false);

    const handleLogout = () => {
        onLogout();
        navigate('/login');
    };

    return (
        <header style={headerStyle}>
            <h1 style={logoStyle}>🩺 HEARTH COM</h1>
            <nav style={navStyle}>
                {isLoggedIn ? (
                    <>
                        <Link to="/" style={linkStyle}>Chat</Link>
                        <Link to="/profile" style={linkStyle}>Profile</Link>
                        <Link to="/news" style={linkStyle}>News Feed</Link>
                        <Link to="/notifications" style={linkStyle}>
                            Notifications {notificationCount > 0 && <span style={badgeStyle}>{notificationCount}</span>}
                        </Link>
                        <button
                            onClick={handleLogout}
                            style={{
                                ...buttonStyle,
                                marginLeft: '15px',
                                ...(isLogoutHovered ? buttonHoverStyle : {})
                            }}
                            onMouseEnter={() => setIsLogoutHovered(true)}
                            onMouseLeave={() => setIsLogoutHovered(false)}
                        >
                            Logout
                        </button>
                    </>
                ) : (
                    <Link to="/login" style={linkStyle}>Login</Link>
                )}
            </nav>
        </header>
    );
};

// Styles for professionalism
const headerStyle = {
    backgroundColor: '#ffffff', // --color-bubble-doctor (white)
    padding: '15px 30px',
    borderBottom: '1px solid #eee',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: 'rgba(0, 0, 0, 0.05) 0px 4px 6px', // --color-shadow
};

const logoStyle = {
    fontSize: '1.8em',
    color: '#007bff', // --color-primary (Medical Blue)
    margin: 0,
    fontWeight: '700',
};

const navStyle = {
    display: 'flex',
    alignItems: 'center',
};

const linkStyle = {
    color: '#333', // --color-text
    textDecoration: 'none',
    fontWeight: '500',
    marginLeft: '20px',
    padding: '5px',
};

const buttonStyle = {
    backgroundColor: '#dc3545',
    color: 'white',
    padding: '8px 15px',
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    fontWeight: '600',
    transition: 'all 0.3s ease',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
};

const buttonHoverStyle = {
    backgroundColor: '#c82333',
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
};

const badgeStyle = {
    backgroundColor: '#ffc107',
    color: '#333', // --color-text
    borderRadius: '50%',
    padding: '2px 8px',
    fontSize: '0.75em',
    marginLeft: '5px',
    fontWeight: '700',
};

export default Header;
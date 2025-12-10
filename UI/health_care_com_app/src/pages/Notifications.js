import React, { useState, useEffect } from 'react';

const Notifications = ({ userId }) => {
    // Placeholder data to show functionality
    const [notifications, setNotifications] = useState([
        { id: 1, message: "Medication Reminder: Please take your Artemether-Lumefantrine dose now.", type: "medication", is_read: false, timestamp: "2025-11-24T10:00:00Z" },
        { id: 2, message: "Doctor's Advice: Your symptoms suggest immediate re-evaluation at a clinic.", type: "hospital", is_read: false, timestamp: "2025-11-24T12:30:00Z" },
        { id: 3, message: "Wellness: Try 30 minutes of light stretching today for joint mobility.", type: "exercise", is_read: true, timestamp: "2025-11-23T08:00:00Z" },
    ]);
    const [hoveredButtonId, setHoveredButtonId] = useState(null);

    // In a real app, this useEffect would fetch unread notifications from the backend
    // useEffect(() => { /* fetchNotifications(userId); */ }, [userId]);

    const markAsRead = (id) => {
        setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
        // Real app: Send update to backend
    };

    const getIcon = (type) => {
        switch (type) {
            case 'medication': return '💊';
            case 'hospital': return '🏥';
            case 'exercise': return '🏃';
            default: return '🔔';
        }
    };

    return (
        <div className="page-container">
            <div style={pageStyle}>
                <h2 style={{ color: '#007bff' }}>Your Health Notifications</h2> {/* --color-primary */}
                {notifications.length === 0 && <p>You have no new notifications.</p>}
                <div style={notificationListStyle}>
                    {notifications.map(n => (
                        <div key={n.id} style={{ ...notificationItemStyle, backgroundColor: n.is_read ? 'white' : '#e0f7fa' }}> {/* --color-bubble-user */}
                            <span style={iconStyle}>{getIcon(n.type)}</span>
                            <div style={{ flexGrow: 1 }}>
                                <p style={{ fontWeight: n.is_read ? 'normal' : 'bold', margin: '0 0 5px 0' }}>{n.message}</p>
                                <small style={{ color: '#666' }}>{new Date(n.timestamp).toLocaleString()}</small>
                            </div>
                            {!n.is_read && (
                                <button
                                    onClick={() => markAsRead(n.id)}
                                    style={{
                                        ...readButtonStyle,
                                        ...(hoveredButtonId === n.id ? readButtonHoverStyle : {}),
                                    }}
                                    onMouseEnter={() => setHoveredButtonId(n.id)}
                                    onMouseLeave={() => setHoveredButtonId(null)}
                                >
                                    Mark as Read
                                </button>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

// Professional Styling
const pageStyle = {
    maxWidth: '100%',    // Remove width constraints
    width: '100%',      // Use full available width
    margin: '30px 0',   // Remove auto margin for horizontal centering
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '10px',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.05)', // --color-shadow
};

const notificationListStyle = {
    marginTop: '20px',
};

const notificationItemStyle = {
    display: 'flex',
    alignItems: 'center',
    padding: '15px',
    marginBottom: '10px',
    borderRadius: '8px',
    borderLeft: '5px solid #007bff', // --color-primary
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
    transition: 'background-color 0.3s',
};

const iconStyle = {
    fontSize: '1.5em',
    marginRight: '15px',
};

const readButtonStyle = {
    background: 'none',
    border: '1px solid #ccc',
    color: '#666',
    padding: '5px 10px',
    marginLeft: '15px',
    fontSize: '0.9em',
    cursor: 'pointer',
    fontWeight: '600',
    transition: 'all 0.3s ease',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    borderRadius: '4px',
};

const readButtonHoverStyle = {
    backgroundColor: '#007bff',
    color: 'white',
    borderColor: '#007bff',
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
};

export default Notifications;
import React, { useState, useEffect } from 'react';

const UserProfile = ({ userId }) => {
    const [profile, setProfile] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        // Fetch real user profile data from the backend
        const fetchProfile = async () => {
            if (!userId) {
                setError("No user ID provided.");
                setIsLoading(false);
                return;
            }

            try {
                const response = await fetch(`http://localhost:8000/users/${userId}`);

                if (!response.ok) {
                    throw new Error('Failed to fetch user profile');
                }

                const userData = await response.json();

                // Structure the data to match what the UI expects
                setProfile({
                    username: userData.username,
                    full_name: userData.full_name,
                    age: userData.age,
                    location: userData.location,
                    recent_uploads: [], // No actual upload data in the current model
                    settings: {
                        notification_frequency: 'Daily', // Default value
                        preferred_language: 'British English', // Default value
                    }
                });
            } catch (err) {
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };

        fetchProfile();
    }, [userId]);

    if (isLoading) {
        return <div className="page-container" style={{ textAlign: 'center', marginTop: '50px' }}>Loading professional profile...</div>;
    }

    if (error) {
        return <div className="page-container" style={{ color: 'red', textAlign: 'center', marginTop: '50px' }}>{error}</div>;
    }
    
    // Professional Styling
    const profileContainerStyle = {
        maxWidth: '100%',    // Remove width constraints
        width: '100%',      // Use full available width
        margin: '30px 0',   // Remove auto margin for horizontal centering
        padding: '30px',
        backgroundColor: 'white',
        borderRadius: '10px',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.05)', // --color-shadow
    };

    const sectionStyle = {
        borderBottom: '1px solid #eee',
        paddingBottom: '20px',
        marginBottom: '20px',
    };

    const detailItemStyle = {
        display: 'flex',
        justifyContent: 'space-between',
        padding: '8px 0',
        borderBottom: '1px dotted #ccc',
    };

    const labelStyle = {
        fontWeight: '600',
        color: '#333', // --color-text
    };

    const valueStyle = {
        color: '#007bff', // --color-primary
    };

    return (
        <div className="page-container">
            <div style={profileContainerStyle}>
                <h2 style={{ color: '#007bff', textAlign: 'center' }}>Patient Profile & Settings</h2> {/* --color-primary */}
                <p style={{ textAlign: 'center', color: '#555' }}>This information is used by Dr. Finch to personalize your virtual care.</p>

                <div style={sectionStyle}>
                    <h3>👤 Personal Details</h3>
                    <div style={detailItemStyle}><span style={labelStyle}>Full Name:</span> <span style={valueStyle}>{profile.full_name}</span></div>
                    <div style={detailItemStyle}><span style={labelStyle}>Age:</span> <span style={valueStyle}>{profile.age} years</span></div>
                    <div style={detailItemStyle}><span style={labelStyle}>Current Location:</span> <span style={valueStyle}>{profile.location}</span></div>
                    <div style={detailItemStyle}><span style={labelStyle}>Username:</span> <span style={valueStyle}>{profile.username}</span></div>
                </div>

                <div style={sectionStyle}>
                    <h3>📂 Uploaded Documents</h3>
                    {profile.recent_uploads.map(doc => (
                         <div key={doc.id} style={detailItemStyle}>
                            <span style={labelStyle}>{doc.name}</span>
                            <a href="#" style={{ color: '#28a745' }}>View/Download</a> {/* --color-secondary */}
                        </div>
                    ))}
                    {profile.recent_uploads.length === 0 && <p style={{ color: '#888' }}>No documents uploaded yet.</p>}
                </div>

                <div>
                    <h3>⚙️ Application Settings</h3>
                    <div style={detailItemStyle}><span style={labelStyle}>Notification Frequency:</span> <span style={valueStyle}>{profile.settings.notification_frequency}</span></div>
                    <div style={detailItemStyle}><span style={labelStyle}>Doctor's Persona Language:</span> <span style={valueStyle}>{profile.settings.preferred_language}</span></div>
                    <button className="primary-btn" style={{ marginTop: '20px', width: '100%' }}>Update Settings</button>
                </div>
            </div>
        </div>
    );
};

export default UserProfile;
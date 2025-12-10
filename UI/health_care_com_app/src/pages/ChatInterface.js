import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import MessageBubble from '../components/MessageBubble';
import UploadModal from '../components/UploadModal';

const ChatInterface = ({ userId, isLoggedIn }) => {
    const [inputMessage, setInputMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [isUploadHovered, setIsUploadHovered] = useState(false);
    const chatEndRef = useRef(null);

    // Initial check and fetch history on component mount
    useEffect(() => {
        if (!isLoggedIn) return;
        // In a real app, you would fetch history here using a separate API endpoint
        // For this demo, we'll start with a generic greeting
        setMessages([
            { sender: 'doctor', content: "Good day. I'm Dr. Alistair Finch. How are you feeling today, and what can I assist you with?" }
        ]);
    }, [isLoggedIn]);

    // Scroll to the bottom on new message
    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim() || isLoading) return;

        const userMsg = { sender: 'user', content: inputMessage };
        setMessages(prev => [...prev, userMsg]);
        setInputMessage('');
        setIsLoading(true);

        try {
            const requestBody = { user_id: userId, message: inputMessage };

            const response = await fetch('http://localhost:8000/chat/message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.response || 'An unknown error occurred with the doctor service.');
            }

            const doctorMsg = { sender: 'doctor', content: data.response };
            setMessages(prev => [...prev, doctorMsg]);

        } catch (error) {
            const errorMsg = { sender: 'doctor', content: `[System Error]: ${error.message}. Please try again.` };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsLoading(false);
        }
    };

    if (!isLoggedIn) {
        return <div className="page-container">
            <p style={{ textAlign: 'center', marginTop: '50px', fontSize: '1.2em' }}>
                Please <Link to="/login" style={{ color: '#007bff' }}>log in</Link> or <Link to="/register" style={{ color: '#007bff' }}>register</Link> to start your consultation. {/* --color-primary */}
            </p>
        </div>
    }

    return (
        <div className="page-container">
            <div style={chatPageStyle}>
                <h2 style={{ textAlign: 'center', color: '#007bff', borderBottom: '1px solid #eee', paddingBottom: '15px' }}> {/* --color-primary */}
                    Your Virtual Consultation with Dr. Finch
                </h2>

                <div style={chatWindowStyle}>
                    {messages.map((msg, index) => (
                        <MessageBubble key={index} sender={msg.sender} content={msg.content} />
                    ))}
                    {isLoading && <MessageBubble sender="doctor" content="Dr. Finch is typing..." />}
                    <div ref={chatEndRef} />
                </div>

                <form onSubmit={handleSendMessage} style={inputAreaStyle}>
                    <button
                        type="button"
                        onClick={() => setIsUploadModalOpen(true)}
                        style={{
                            ...uploadButtonStyle,
                            ...(isUploadHovered ? uploadButtonHoverStyle : {})
                        }}
                        title="Upload Medical Documents"
                        onMouseEnter={() => setIsUploadHovered(true)}
                        onMouseLeave={() => setIsUploadHovered(false)}
                    >
                        📎
                    </button>
                    <input
                        type="text"
                        style={textInputStyle}
                        placeholder="Tell Dr. Finch how you are feeling or describe your symptoms..."
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        disabled={isLoading}
                    />
                    <button type="submit" className="primary-btn" disabled={isLoading || !inputMessage.trim()}>
                        Send
                    </button>
                </form>

                <UploadModal
                    isOpen={isUploadModalOpen}
                    onClose={() => setIsUploadModalOpen(false)}
                    userId={userId}
                />
            </div>
        </div>
    );
};

// Professional Styling
const chatPageStyle = {
    display: 'flex',
    flexDirection: 'column',
    height: 'calc(100vh - 80px)', // Account for header
    padding: '20px',
    width: '100%',      // Use full available width
    maxWidth: '100%',   // Remove any width constraints
    margin: '0',        // Remove auto margin
};

const chatWindowStyle = {
    flexGrow: 1,
    overflowY: 'auto',
    padding: '15px',
    backgroundColor: '#f4f6f9', // --color-bg-light
    border: '1px solid #ddd',
    borderRadius: '10px',
    display: 'flex',
    flexDirection: 'column',
    marginBottom: '15px',
};

const inputAreaStyle = {
    display: 'flex',
    padding: '10px',
    backgroundColor: 'white',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
};

const textInputStyle = {
    flexGrow: 1,
    border: 'none',
    padding: '10px 15px',
    fontSize: '1em',
    marginRight: '10px',
    borderRadius: '6px',
    backgroundColor: '#f9f9f9',
};

const uploadButtonStyle = {
    fontSize: '1.2em',
    marginRight: '10px',
    backgroundColor: '#fff',
    color: '#007bff', // --color-primary
    border: '1px solid #007bff', // --color-primary
    borderRadius: '6px',
    cursor: 'pointer',
    fontWeight: '600',
    transition: 'all 0.3s ease',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
};

const uploadButtonHoverStyle = {
    backgroundColor: '#007bff',
    color: 'white',
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
};

export default ChatInterface;
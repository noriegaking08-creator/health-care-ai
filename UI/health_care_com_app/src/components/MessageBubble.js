import React from 'react';

const MessageBubble = ({ sender, content }) => {
    const isDoctor = sender === 'doctor';
    const bubbleStyle = {
        maxWidth: '70%',
        padding: '12px 18px',
        borderRadius: isDoctor ? '18px 18px 18px 4px' : '18px 18px 4px 18px',
        marginBottom: '10px',
        backgroundColor: isDoctor ? '#ffffff' : '#e0f7fa', // --color-bubble-doctor : --color-bubble-user
        alignSelf: isDoctor ? 'flex-start' : 'flex-end',
        boxShadow: 'rgba(0, 0, 0, 0.05) 0px 1px 3px', // --color-shadow
        border: isDoctor ? '1px solid #eee' : 'none',
        wordBreak: 'break-word',
    };

    const senderStyle = {
        fontSize: '0.8em',
        color: isDoctor ? '#007bff' : '#555', // --color-primary : default
        fontWeight: 'bold',
        marginBottom: '5px',
    };

    return (
        <div style={{ display: 'flex', width: '100%', justifyContent: isDoctor ? 'flex-start' : 'flex-end' }}>
            <div style={bubbleStyle}>
                <div style={senderStyle}>
                    {isDoctor ? 'Dr. Alistair Finch' : 'You'}
                </div>
                {content}
            </div>
        </div>
    );
};

export default MessageBubble;
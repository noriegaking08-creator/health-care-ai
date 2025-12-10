import React, { useState } from 'react';

const UploadModal = ({ isOpen, onClose, userId }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState('');
    const [isCancelHovered, setIsCancelHovered] = useState(false);

    if (!isOpen) return null;

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setUploadStatus('');
    };

    const handleUpload = async () => {
        if (!selectedFile || !userId) {
            setUploadStatus('Please select a file first.');
            return;
        }

        setUploading(true);
        setUploadStatus(`Uploading ${selectedFile.name}...`);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            // API call to the backend upload endpoint
            const response = await fetch(`http://localhost:8000/data/upload/${userId}`, {
                method: 'POST',
                // Note: fetch will automatically set Content-Type: multipart/form-data
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Upload failed on server.');
            }

            const result = await response.json();
            setUploadStatus(`Success: ${result.message}`);
            setTimeout(onClose, 2000);

        } catch (error) {
            setUploadStatus(`Upload Error: ${error.message}`);
        } finally {
            setUploading(false);
            setSelectedFile(null);
        }
    };

    // Modal styling for a focused professional look
    const modalStyle = {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
    };

    const contentStyle = {
        backgroundColor: 'white',
        padding: '30px',
        borderRadius: '10px',
        width: '400px',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
        textAlign: 'center',
    };

    return (
        <div style={modalStyle}>
            <div style={contentStyle}>
                <h3>Medical Document Upload 📂</h3>
                <p>Securely upload X-Rays, Lab Reports, or any other relevant medical data.</p>
                <input type="file" onChange={handleFileChange} style={{ marginBottom: '20px' }} disabled={uploading} />
                <button
                    className="primary-btn"
                    onClick={handleUpload}
                    disabled={!selectedFile || uploading}
                    style={{ display: 'block', width: '100%', marginBottom: '10px' }}
                >
                    {uploading ? 'Processing...' : 'Upload & Send to Doctor'}
                </button>
                <button
                    onClick={onClose}
                    style={{
                        background: 'none',
                        color: '#555',
                        padding: '8px 16px',
                        border: '1px solid #ccc',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontWeight: '600',
                        transition: 'all 0.3s ease',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                        ...(isCancelHovered ? {
                            backgroundColor: '#f5f5f5',
                            transform: 'translateY(-2px)',
                            boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
                        } : {})
                    }}
                    onMouseEnter={() => setIsCancelHovered(true)}
                    onMouseLeave={() => setIsCancelHovered(false)}
                >
                    Cancel
                </button>
                {uploadStatus && <p style={{ marginTop: '15px', color: uploading ? '#007bff' : (uploadStatus.includes('Success') ? '#28a745' : 'red') }}>{uploadStatus}</p>} // --color-primary : --color-secondary
            </div>
        </div>
    );
};

export default UploadModal;
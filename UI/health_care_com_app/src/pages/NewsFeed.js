import React, { useState, useEffect } from 'react';

const NewsFeed = () => {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Simulated news data for health in Malawi
    useEffect(() => {
        // In a real app, this would fetch from a news API
        const mockData = [
            {
                id: 1,
                title: "New Malaria Prevention Program Launched",
                summary: "Ministry of Health launches new initiative focusing on preventive measures in rural areas.",
                source: "Malawi Ministry of Health",
                date: "2025-11-24",
                category: "Malaria"
            },
            {
                id: 2,
                title: "Nutrition Guidelines Updated for Malawi Population",
                summary: "Updated dietary recommendations released to address malnutrition in children under 5.",
                source: "WHO Malawi",
                date: "2025-11-22",
                category: "Wellness"
            },
            {
                id: 3,
                title: "Cholera Outbreak Response Update",
                summary: "Health officials report containment efforts showing positive results in affected districts.",
                source: "CDC Malawi",
                date: "2025-11-20",
                category: "Outbreak"
            },
            {
                id: 4,
                title: "Telemedicine Access Improved in Rural Areas",
                summary: "New initiatives to expand digital health services to remote communities.",
                source: "ICT Ministry",
                date: "2025-11-18",
                category: "Technology"
            }
        ];

        // Simulate API fetch time
        setTimeout(() => {
            setArticles(mockData);
            setLoading(false);
        }, 800);
    }, []);

    const categoryColors = {
        'Malaria': '#e74c3c',
        'Wellness': '#27ae60',
        'Outbreak': '#e67e22',
        'Technology': '#3498db'
    };

    if (loading) {
        return (
            <div className="page-container" style={{ textAlign: 'center', marginTop: '50px' }}>
                Loading health news...
            </div>
        );
    }

    if (error) {
        return (
            <div className="page-container" style={{ color: 'red', textAlign: 'center', marginTop: '50px' }}>
                {error}
            </div>
        );
    }

    // Professional Styling
    const containerStyle = {
        maxWidth: '100%',    // Remove width constraints
        width: '100%',      // Use full available width
        margin: '30px 0',   // Remove auto margin for horizontal centering
        padding: '20px',
        backgroundColor: 'white',
        borderRadius: '10px',
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.05)', // --color-shadow
    };

    const articleStyle = {
        borderBottom: '1px solid #eee',
        marginBottom: '25px',
        paddingBottom: '25px',
    };

    const titleStyle = {
        color: '#007bff', // --color-primary
        fontSize: '1.4em',
        margin: '0 0 10px 0',
    };

    const metaStyle = {
        display: 'flex',
        justifyContent: 'space-between',
        color: '#666',
        fontSize: '0.9em',
        marginBottom: '10px',
    };

    const categoryStyle = {
        display: 'inline-block',
        padding: '3px 10px',
        borderRadius: '12px',
        fontSize: '0.8em',
        fontWeight: 'bold',
    };

    const summaryStyle = {
        lineHeight: '1.6',
        color: '#333', // --color-text
    };

    return (
        <div className="page-container">
            <div style={containerStyle}>
                <h2 style={{ color: '#007bff', textAlign: 'center' }}>Health News & Updates</h2> {/* --color-primary */}
                <p style={{ textAlign: 'center', color: '#555', marginBottom: '30px' }}>
                    Stay updated on health information relevant to Malawi
                </p>

                {articles.length > 0 ? (
                    articles.map(article => (
                        <div key={article.id} style={articleStyle}>
                            <div style={metaStyle}>
                                <span style={{ ...categoryStyle, backgroundColor: `${categoryColors[article.category]}20`, color: categoryColors[article.category] }}>
                                    {article.category}
                                </span>
                                <span>{article.date} | {article.source}</span>
                            </div>
                            <h3 style={titleStyle}>{article.title}</h3>
                            <p style={summaryStyle}>{article.summary}</p>
                            <button className="primary-btn" style={{ marginTop: '10px' }}>
                                Read Full Article
                            </button>
                        </div>
                    ))
                ) : (
                    <p style={{ textAlign: 'center', color: '#666' }}>No health news available at the moment.</p>
                )}
            </div>
        </div>
    );
};

export default NewsFeed;
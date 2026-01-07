# HealthCare AI Deployment Guide

## Architecture Overview

This is a FastAPI-based healthcare application with AI-powered medical consultation:
- **Backend**: FastAPI application that handles API requests, authentication, and database interactions
- **AI Integration**: Hugging Face API for medical consultation with fallback system
- **Database**: SQLAlchemy ORM with PostgreSQL support for production

## Deployment Strategy

The application is designed for deployment on Render as a web service:

### Deployment Platforms
- **Render** (Primary - recommended)
- **Railway**
- **Heroku**
- **DigitalOcean App Platform**

## Backend Deployment Instructions

### 1. Database Setup (PostgreSQL Recommended)

First, create a PostgreSQL database using your preferred provider:
- **Render**: Can provision a PostgreSQL add-on
- **Railway**: Built-in PostgreSQL
- **Heroku**: Heroku Postgres addon

### 2. Environment Variables

Set these environment variables in your deployment platform:

```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
HF_API_KEY=your_huggingface_api_token
ENVIRONMENT=production
```

### 3. Deployment Steps

#### Render (Recommended)

1. Create an account at [Render](https://render.com)
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Render will automatically detect the Python application from `render.yaml`
5. Set runtime to "Python"
6. Build command: `pip install -r requirements.txt` (auto-detected from render.yaml)
7. Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT` (auto-configured in render.yaml)
8. Add environment variables in the Render dashboard:
   - `DATABASE_URL`: PostgreSQL database URL
   - `HF_API_KEY`: Hugging Face API token
   - `ENVIRONMENT`: production
9. Deploy automatically on push to GitHub

#### Railway

1. Create an account at [Railway](https://railway.app)
2. Create a new project and connect your GitHub repository
3. Add PostgreSQL database via "Database" → "Add Database"
4. Set environment variables in "Variables" tab
5. Deploy automatically on push

#### Heroku

1. Create an account at [Heroku](https://heroku.com)
2. Create a new app
3. Add Heroku Postgres addon
4. Go to Settings → Config Vars and add environment variables
5. Deploy via GitHub integration:
   - Enable automatic deploys from GitHub
   - Set environment variables in Config Vars

## Configuration Details

### API Endpoints

The application provides these endpoints:
- `POST /users/register` - User registration
- `POST /users/login` - User authentication
- `GET /users/{user_id}` - Get user profile
- `POST /chat/message` - AI medical consultation
- `GET /health` - Health check

### CORS Configuration

The backend is configured to allow requests from any origin during development, but this should be restricted in production.

### Database Migration

On first deployment, the application will automatically create the required database tables using SQLAlchemy's create_all() function.

## Production Considerations

### Security
- Never commit API keys to the repository
- Use HTTPS for all production endpoints
- The bcrypt implementation provides secure password hashing
- CORS is configured to allow necessary origins

### Performance
- SQLAlchemy connection pooling handles concurrent requests
- Hugging Face API integration with timeout handling
- Proper error handling and fallback responses

### AI Integration
- Primary: Hugging Face medical model (MedAlpaca-7b)
- Fallback: Rule-based medical advice system
- API timeout and error handling built-in

## Troubleshooting

### Common Issues

1. **Database Connection Issues**: Ensure your `DATABASE_URL` is correct and accessible
2. **API Communication**: Verify that `HF_API_KEY` is set correctly
3. **CORS Errors**: Check CORS configuration in main.py
4. **Model API Failures**: The fallback system will handle Hugging Face API issues

### Health Check

Use the `/health` endpoint to verify application status: `https://your-app.onrender.com/health`

### Logging

Check your platform's logs for any deployment or runtime errors.

## Updating the Application

### Updates
- Push changes to your connected GitHub repository
- Platform will automatically redeploy (if configured)

## Architecture Diagram

```
[User's Client]
        ↓ (HTTPS)
[Frontend Application]
        ↓ (API Request)
[HealthCare AI Backend on Render]
        ↓ (Hugging Face API / Fallback)
[AI Medical Consultation]
        ↓ (Database Connection)
[PostgreSQL Database]
```

This architecture provides a scalable, production-ready healthcare consultation system.
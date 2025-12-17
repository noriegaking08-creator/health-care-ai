# HealthCo Deployment Guide

## Architecture Overview

This is a two-part application:
- **Backend**: FastAPI application that handles API requests, authentication, and database interactions
- **Frontend**: React application that serves the user interface

## Deployment Strategy

The backend and frontend must be deployed separately due to Vercel's limitations with FastAPI applications:

### Backend Deployment Options
- **Railway** (Recommended)
- **Render**
- **Heroku**
- **DigitalOcean App Platform**
- **AWS (Elastic Beanstalk, ECS, EC2)**
- **Google Cloud Platform**

### Frontend Deployment
- **Vercel** (Primary choice for React apps)

## Backend Deployment Instructions

### 1. Database Setup (PostgreSQL Recommended)

First, create a PostgreSQL database using your preferred provider:
- **Railway**: Built-in PostgreSQL
- **Render**: External database or managed
- **Heroku**: Heroku Postgres addon

### 2. Environment Variables

Set these environment variables in your deployment platform:

```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
ZHIPU_API_KEY=your_zhipu_api_key
ENVIRONMENT=production
```

### 3. Deployment Steps

#### Option A: Railway (Recommended)

1. Create an account at [Railway](https://railway.app)
2. Create a new project and connect your GitHub repository
3. Add PostgreSQL database via "Database" → "Add Database"
4. Set environment variables in "Variables" tab
5. Deploy automatically on push

#### Option B: Render

1. Create an account at [Render](https://render.com)
2. Create a new "Web Service" 
3. Connect your GitHub repository
4. Set runtime to "Python"
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `gunicorn api.main:app -c gunicorn_config.py`
7. Add environment variables
8. For database, use "Dashboard" → "New" → "External Database" and connect PostgreSQL

#### Option C: Heroku

1. Create an account at [Heroku](https://heroku.com)
2. Create a new app
3. Add Heroku Postgres addon
4. Go to Settings → Config Vars and add environment variables
5. Deploy via GitHub integration or CLI:
   ```bash
   heroku create your-app-name
   heroku config:set DATABASE_URL=your_db_url
   heroku config:set ZHIPU_API_KEY=your_api_key
   heroku config:set ENVIRONMENT=production
   git push heroku main
   ```

## Frontend Deployment to Vercel

### Prerequisites
- Your backend must be deployed and accessible via HTTPS
- Note the backend URL (e.g., `https://your-backend.onrender.com`)

### Steps

1. Go to [Vercel](https://vercel.com) and sign in
2. "New Project" → Import your GitHub repository
3. In "Environment Variables" section, add:
   - `REACT_APP_API_URL`: The URL of your deployed backend (e.g., `https://your-backend-app.onrender.com`)
4. Set build settings:
   - Framework: Create React App
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `build` (auto-detected)
5. Click "Deploy"

## Configuration Details

### API Endpoints

The frontend will make requests to:
- `https://your-backend.com/users/register`
- `https://your-backend.com/users/login`
- `https://your-backend.com/users/{user_id}`
- `https://your-backend.com/chat/message`
- `https://your-backend.com/data/upload/{user_id}`

### CORS Configuration

The backend is configured to allow requests from common local development ports and can be expanded for production domains.

### Database Migration

On first deployment, the application will automatically create the required database tables. The `init_db()` function in `database_manager.py` handles this.

## Production Considerations

### Security
- Never commit API keys to the repository
- Use HTTPS for all production endpoints
- The current bcrypt implementation provides secure password hashing
- CORS is properly configured to prevent unauthorized access

### Performance
- PostgreSQL connection pooling is configured in `database_manager.py`
- Gunicorn workers can be adjusted based on load
- File upload size is limited to 5MB

### Scalability
- The application can be scaled horizontally using multiple workers
- Database connection pooling handles concurrent requests
- Session management is handled through database and JWT tokens

## Troubleshooting

### Common Issues

1. **Database Connection Issues**: Ensure your `DATABASE_URL` is correct and accessible
2. **CORS Errors**: Check that your frontend domain is included in the CORS allowlist
3. **API Communication**: Verify that `REACT_APP_API_URL` is set correctly in the frontend environment
4. **File Upload Failures**: Ensure the upload directory is writable (though for production use cloud storage)

### Health Check

Use the `/health` endpoint to verify backend status: `https://your-backend.com/health`

### Logging

Check your platform's logs for any deployment or runtime errors.

## Updating the Application

### Backend Updates
- Push changes to your connected GitHub repository
- Platform will automatically redeploy (if configured)

### Frontend Updates
- Push changes to your connected GitHub repository
- Vercel will automatically build and deploy

## Architecture Diagram

```
[User's Browser] 
        ↓ (HTTPS)
[Frontend on Vercel]
        ↓ (Environment Variable - API URL)
[Backend on Railway/Render/Heroku]
        ↓ (Database Connection)
[PostgreSQL Database]
```

This architecture ensures scalability and separation of concerns while working within Vercel's limitations for FastAPI applications.
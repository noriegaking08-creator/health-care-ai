# HealthCare AI Environment Setup

## Setting up Environment Variables for Production Deployment

### 1. Create a `.env` file for local development (do NOT commit this to git)
```
HF_API_KEY=your_huggingface_api_token_here
DATABASE_URL=sqlite:///./healthcare.db
ENVIRONMENT=development
```

### 2. Add `.env` to your `.gitignore` (already done in this project)
This ensures your tokens are never exposed in the repository.

### 3. Configure environment variables in your deployment platform (Render, Railway, etc.)

For Render deployment:

1. Go to your service in the Render dashboard
2. Navigate to "Environment" → "Environment Variables"
3. Add these variables:
   - Key: `HF_API_KEY`, Value: `your_huggingface_api_token_here`
   - Key: `DATABASE_URL`, Value: `your_postgresql_database_url`
   - Key: `ENVIRONMENT`, Value: `production`
4. Save the changes
5. Redeploy your service for changes to take effect

### 4. Environment Variables Configuration:
In your deployment platform dashboard:
- Add: `HF_API_KEY` = your Hugging Face API token
- Add: `DATABASE_URL` = your PostgreSQL database connection string
- Add: `ENVIRONMENT` = production
- Apply to all deployments

### 5. Security Notes:
- Never share your Hugging Face token publicly
- Always use environment variables for sensitive data
- The token is only used server-side (not exposed to frontend)
- If your token is compromised, regenerate it in your Hugging Face account
- Use strong, unique passwords for database connections

### 6. Database Configuration:
- For local development: Use SQLite with `DATABASE_URL=sqlite:///./healthcare.db`
- For production: Use PostgreSQL with `DATABASE_URL=postgresql://user:password@host:port/database_name`
- The application automatically handles the PostgreSQL URL format conversion

### 7. Testing the API:
Once deployed with the HF_API_KEY, your medical consultations will use the Hugging Face medical model for more accurate responses. Without the token, it will fall back to rule-based responses.
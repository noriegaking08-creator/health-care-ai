# HealthCom Deployment Guide

## Setting up Environment Variables for Vercel Deployment

### 1. Create a `.env` file for local development (do NOT commit this to git)
```
HF_API_KEY=your_huggingface_api_token_here
```

### 2. Add `.env` to your `.gitignore` (already done in this project)
This ensures your token is never exposed in the repository.

### 3. Configure environment variables in Vercel Dashboard
When you deploy to Vercel:

1. Go to your project in the Vercel dashboard
2. Navigate to "Settings" → "Environment Variables"
3. Add a new variable:
   - Key: `HF_API_KEY`
   - Value: `your_huggingface_api_token_here`
4. Save the changes
5. Redeploy your project for changes to take effect

### 4. Vercel Environment Variables Configuration:
In your Vercel project dashboard:
- Go to Settings → Environment Variables
- Add: `HF_API_KEY` = `your_huggingface_api_token_here`
- Apply to all deployments (Development, Preview, Production)

### 5. Security Notes:
- Never share your Hugging Face token publicly
- Always use environment variables for sensitive data
- The token is only used server-side in API routes (not exposed to frontend)
- If your token is compromised, regenerate it in your Hugging Face account

### 6. Testing the API:
Once deployed with the token, your medical Q&A will use the Hugging Face model for more accurate responses. Without the token, it will fall back to rule-based responses.
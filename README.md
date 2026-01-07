# HealthCare AI - Personal Healthcare Assistant

A modern, personalized healthcare web application with AI-powered medical consultation. Get professional medical advice and personalized health consultations anytime, anywhere.

## 🚀 Features

- **User Authentication**: Secure login and registration system
- **AI-Powered Chat**: Intelligent health consultation with Dr. Alistair Finch using Hugging Face models
- **Personalized Profile**: Manage your health information and preferences
- **Database Integration**: Full user management and conversation history
- **Production Ready**: Optimized for deployment on Render

## 📁 Project Structure

```
health-care-ai/
├── server.py           # Application entry point
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment configuration
├── .gitignore        # Git ignore rules
├── README.md         # Project documentation
├── DEPLOYMENT.md     # Deployment instructions
├── ENVIRONMENT_SETUP.md # Environment setup guide
├── backend/
│   ├── main.py       # FastAPI application
│   ├── models.py     # Database models
│   ├── auth.py       # Authentication functions
│   └── ai_doctor.py  # AI consultation logic
└── public/           # Frontend files (HTML, CSS, JS)
    ├── index.html
    ├── login.html
    ├── register.html
    ├── chat.html
    ├── profile.html
    ├── css/
    └── js/
```

## 🚀 Quick Start

### For Local Development:

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd health-care-ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with:
   ```env
   HF_API_KEY=your_huggingface_api_token_here
   DATABASE_URL=sqlite:///./healthcare.db
   ENVIRONMENT=development
   ```

4. **Run the application**:
   ```bash
   python server.py
   ```

5. **Access the application** at `http://localhost:8000`

## 🌐 Render Deployment

This app is optimized for Render deployment:

1. **Push your code to GitHub**
2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Create a new "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the Python application from `render.yaml`
3. **Set environment variables** in Render dashboard:
   - `DATABASE_URL`: Your PostgreSQL database URL
   - `HF_API_KEY`: Your Hugging Face API token
   - `ENVIRONMENT`: production
4. **Your API is live!**

## 🔧 API Endpoints

- `POST /users/register` - Register a new user
- `POST /users/login` - User login
- `GET /users/{user_id}` - Get user profile
- `POST /chat/message` - Chat with AI doctor
- `GET /health` - Health check endpoint

## 🛠️ Technologies Used

- **Backend**: FastAPI, SQLAlchemy, Python
- **Database**: PostgreSQL (production) / SQLite (development)
- **AI Model**: Hugging Face (MedAlpaca-7b medical model)
- **Authentication**: bcrypt password hashing
- **Deployment**: Render with automatic deployment from GitHub

## 🔐 Environment Variables

For production deployment, configure these environment variables:

```env
HF_API_KEY=your_huggingface_api_token_here
DATABASE_URL=postgresql://username:password@host:port/database_name
ENVIRONMENT=production
```

Get your Hugging Face API token from [Hugging Face Settings](https://huggingface.co/settings/tokens).

## 🚀 Production Features

- **Scalable Architecture**: Designed for cloud deployment
- **Secure Authentication**: Proper password hashing and session management
- **AI Integration**: Medical-specific model with fallback responses
- **Database Management**: Full ORM with migration-ready schema
- **Health Monitoring**: Built-in health check endpoint

## 📞 Support

For support, please open an issue in the GitHub repository.

## 📄 License

This project is licensed under the MIT License.
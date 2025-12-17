# HealthCom - Personal Healthcare Assistant

A modern, personalized healthcare web application built with pure HTML, CSS, and JavaScript. Get professional medical advice and personalized health consultations anytime, anywhere.

## 🚀 Features

- **User Authentication**: Secure login and registration system
- **AI-Powered Chat**: Intelligent health consultation with Dr. Alistair Finch
- **Personalized Profile**: Manage your health information and preferences
- **Responsive Design**: Works perfectly on all devices
- **Fast & Lightweight**: Optimized for speed and performance
- **Easy Deployment**: Ready for Vercel deployment through GitHub

## 📁 Project Structure

```
healthcom/
├── index.html          # Home page
├── login.html          # Login page
├── register.html       # Registration page
├── chat.html           # Main chat interface
├── profile.html        # User profile page
├── css/
│   └── style.css       # Main stylesheet
├── js/
│   ├── api.js          # API and session management
│   ├── auth.js         # Authentication functions
│   ├── chat.js         # Chat functionality
│   └── main.js         # Main application logic
└── vercel.json         # Vercel configuration
```

## 🚀 Quick Start

### For Development:

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd healthcom
   ```

2. **Open `index.html` in your browser** to start the app

3. **The app includes mock API functionality** for immediate testing

### For Production (with real backend):

1. **Deploy your backend API** to a server (e.g., Railway, Render, Heroku)

2. **Update `js/api.js`** to point to your backend URL:
   ```javascript
   const API_BASE_URL = 'https://your-backend-url.com';
   ```

## 🔧 API Integration

The app includes smart API handling:

- **Automatic fallback**: Uses mock API if backend is unreachable
- **Session management**: Stores user data in localStorage
- **Error handling**: Graceful error messages for users
- **Real-time chat**: Interactive health consultations

## 🌐 Vercel Deployment

This app is optimized for Vercel deployment:

1. **Push your code to GitHub**
2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will automatically detect and deploy your static site
3. **Your site is live!**

## 💡 Key Improvements

- **Simplified Architecture**: Single codebase with no complex dependencies
- **Better Performance**: Lightweight with fast loading times
- **Mobile-First Design**: Responsive and optimized for mobile
- **Enhanced UX**: Smooth animations and intuitive interface
- **Personalized**: Tailored user experience and health advice
- **Secure**: Proper session management and input validation
- **Maintainable**: Clean, well-organized code structure

## 🛠️ Technologies Used

- **Frontend**: Pure HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS with flexbox/grid and animations
- **API**: RESTful API integration
- **Deployment**: Optimized for Vercel static hosting
- **Icons**: Font Awesome for beautiful icons

## 📱 Features

- **Health Consultation**: Chat with AI doctor for medical advice
- **User Profiles**: Personalized health information
- **Secure Authentication**: Safe login and registration
- **Real-time Messaging**: Instant health consultations
- **Responsive Design**: Perfect on desktop, tablet, and mobile
- **Offline Support**: Basic functionality available offline

## 🔐 Environment Variables

To run this application with full backend functionality, create a `.env` file in the root directory with the following variables:

```env
HF_API_KEY=your_huggingface_api_token_here
DATABASE_URL=sqlite:///./healthcom.db
ENVIRONMENT=development
```

Get your Hugging Face API token from [Hugging Face Settings](https://huggingface.co/settings/tokens).

## 🎨 Customization

Easy to customize the look and feel:

- **Colors**: Modify CSS variables in `style.css`
- **Logo**: Change the navbar logo and favicon
- **Content**: Update text content in HTML files
- **Behaviors**: Modify JavaScript for custom functionality

## 🚀 Performance Tips

- **Image Optimization**: Use WebP format for images
- **CSS Optimization**: Minify CSS in production
- **JavaScript Bundling**: Consider bundling in future updates
- **CDN**: Serve assets via CDN for faster loading

## 📞 Support

For support, please open an issue in the GitHub repository.

## 📄 License

This project is licensed under the MIT License.
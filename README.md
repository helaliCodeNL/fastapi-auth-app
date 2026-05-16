# FastAPI Authentication System

Complete authentication system with Login, Register, Password Reset, and 2FA.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL

### 1. Database Setup

**Option A: Using Docker**
```bash
docker run -d --name postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=fastapi_auth \
  -p 5432:5432 \
  postgres:15
```

**Option B: Create Manually**
```sql
CREATE DATABASE fastapi_auth;
CREATE USER "user" WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_auth TO "user";
```

### 2. Backend Setup

```bash
cd backend

# Create venv
python -m venv venv

# Activate venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Edit .env and update DATABASE_URL

# Run server
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000
API Docs at: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend runs at: http://localhost:3000

## 📋 Features

✅ User Registration (email, name, phone, password)
✅ User Login (email, password)
✅ JWT Authentication (access & refresh tokens)
✅ Two-Factor Authentication (2FA with QR codes)
✅ Password Reset (email-based)
✅ Forgot Password
✅ User Profile
✅ Security Best Practices

## 🔐 API Endpoints

### Auth
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/auth/setup-2fa` - Setup 2FA
- `POST /api/auth/verify-2fa` - Verify 2FA code
- `POST /api/auth/login-2fa` - Login with 2FA
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password
- `POST /api/auth/refresh` - Refresh access token

### Users
- `GET /api/users/me` - Get profile
- `POST /api/users/disable-2fa` - Disable 2FA

## 🔑 Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_auth
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
```

## 📖 Technology Stack

**Backend**
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- PyOTP (2FA)
- python-jose (JWT)
- passlib (Password hashing)

**Frontend**
- React
- Vite
- Axios
- React Router

## 🧪 Test the App

1. Register at http://localhost:3000
2. Login with credentials
3. Setup 2FA (scan with Google Authenticator)
4. Use dashboard

## 🚀 Deployment

See DEPLOYMENT.md for deployment guides.

## 📝 License

MIT

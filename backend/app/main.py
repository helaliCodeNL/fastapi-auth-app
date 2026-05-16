from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine
from app.models.user import Base
from app.api.routes import auth, users

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Auth",
    description="Complete Authentication System with 2FA",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "FastAPI Auth API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

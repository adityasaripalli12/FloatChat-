import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.middleware.security_headers import SecurityHeadersMiddleware

# Import database connection and models to ensure they are created
from backend.database.connection import Base, engine, SessionLocal
from backend.models.user import User
from backend.models.audit import AuditLog
from backend.models.chat import ChatHistory
from backend.models.dataset import Dataset
from backend.models.embedding import Embedding
from backend.models.security import SecurityEvent
from backend.auth.password import hash_password

# Import routers
from backend.routers.auth_router import router as auth_router
from backend.routers.users_router import router as users_router
from backend.routers.datasets_router import router as datasets_router
from backend.routers.visualization_router import router as visualization_router
from backend.routers.chat_router import router as chat_router
from backend.routers.security_router import router as security_router
from backend.routers.audit_router import router as audit_router

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

# Seed default database users if they don't exist
db = SessionLocal()
try:
    admin_user = db.query(User).filter(User.role == "Admin").first()
    if not admin_user:
        new_admin = User(
            name="System Administrator",
            email="admin@argo.edu",
            password_hash=hash_password("admin123"),
            role="Admin",
            is_active=True
        )
        db.add(new_admin)
    
    researcher_user = db.query(User).filter(User.role == "Researcher").first()
    if not researcher_user:
        new_researcher = User(
            name="Dr. Sarah Jenkins",
            email="sarah.jenkins@argo.edu",
            password_hash=hash_password("researcher123"),
            role="Researcher",
            is_active=True
        )
        db.add(new_researcher)

    db.commit()
except Exception as e:
    db.rollback()
    print(f"Error seeding database: {e}")
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Include routers under /api/v1 prefix
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(datasets_router, prefix=settings.API_V1_STR)
app.include_router(visualization_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(security_router, prefix=settings.API_V1_STR)
app.include_router(audit_router, prefix=settings.API_V1_STR)

# Also include routers at root for frontend compatibility
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(datasets_router)
app.include_router(visualization_router)
app.include_router(chat_router)
app.include_router(security_router)
app.include_router(audit_router)

@app.get("/")
def read_root():
    return {
        "message": "FloatChat Enterprise API is running",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint for Render and monitoring services."""
    return {"status": "ok"}

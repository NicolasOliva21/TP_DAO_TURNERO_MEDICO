from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.db.seed import seed

from app.api.routes import auth, patients, doctors, specialties, appointments, reports

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # DB init
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)

    # Routers
    app.include_router(auth.router)
    app.include_router(patients.router)
    app.include_router(doctors.router)
    app.include_router(specialties.router)
    app.include_router(appointments.router)
    app.include_router(reports.router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()

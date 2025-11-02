from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import LoginIn, TokenOut
from app.services.auth_service import AuthService
from app.api.deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    token, user = AuthService.login(db, payload.email, payload.password)
    return {"token": token, "user": user}

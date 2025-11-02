from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, create_access_token

class AuthService:
    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Credenciales inválidas")
        token = create_access_token(str(user.id))
        return token, {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

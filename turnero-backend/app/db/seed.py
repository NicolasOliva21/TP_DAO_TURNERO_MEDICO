from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.models.specialty import Specialty
from app.models.doctor import Doctor

def seed(db: Session):
    # Usuario admin
    if not db.query(User).first():
        admin = User(email="admin@demo.com", name="Admin", hashed_password=hash_password("admin123"), role="admin")
        db.add(admin)

    # Especialidades base
    if not db.query(Specialty).first():
        db.add_all([
            Specialty(nombre="Clínica Médica", descripcion="Consultas generales", activa=True),
            Specialty(nombre="Pediatría", descripcion="Atención niños/as", activa=True),
            Specialty(nombre="Cardiología", descripcion="Sistema cardiovascular", activa=True),
        ])

    # Médico demo
    if not db.query(Doctor).first():
        d = Doctor(
            nombre="Juan", apellido="Pérez", dni="20123456",
            email="juan.perez@demo.com", telefono="351-555-1234",
            matricula="MAT-1234", activo=True
        )
        db.add(d)
    db.commit()

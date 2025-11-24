"""
Patrón Unit of Work para gestión transaccional.
Coordina múltiples repositorios en una sola transacción.
"""
from typing import Optional

from sqlalchemy.orm import Session

from src.repositories.consulta_repository import ConsultaRepository
from src.repositories.database import DatabaseManager
from src.repositories.disponibilidad_repository import (
    BloqueoMedicoRepository,
    DisponibilidadMedicoRepository,
)
from src.repositories.especialidad_repository import EspecialidadRepository
from src.repositories.estado_turno_repository import EstadoTurnoRepository
from src.repositories.medico_repository import MedicoRepository
from src.repositories.paciente_repository import PacienteRepository
from src.repositories.receta_repository import ItemRecetaRepository, RecetaRepository
from src.repositories.recordatorio_repository import RecordatorioRepository
from src.repositories.turno_repository import TurnoRepository


class UnitOfWork:
    """
    Unit of Work: gestiona transacciones y coordina repositorios.
    Implementa context manager para garantizar commit/rollback.
    """

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """
        Args:
            db_manager: Gestor de base de datos (usa el singleton si no se provee)
        """
        self.db_manager = db_manager or DatabaseManager()
        self.session: Optional[Session] = None
        
        # Repositorios (se inicializan al entrar al context)
        self.pacientes: Optional[PacienteRepository] = None
        self.medicos: Optional[MedicoRepository] = None
        self.especialidades: Optional[EspecialidadRepository] = None
        self.estados_turno: Optional[EstadoTurnoRepository] = None
        self.turnos: Optional[TurnoRepository] = None
        self.disponibilidades: Optional[DisponibilidadMedicoRepository] = None
        self.bloqueos: Optional[BloqueoMedicoRepository] = None
        self.consultas: Optional[ConsultaRepository] = None
        self.recetas: Optional[RecetaRepository] = None
        self.items_receta: Optional[ItemRecetaRepository] = None
        self.recordatorios: Optional[RecordatorioRepository] = None

    def __enter__(self) -> "UnitOfWork":
        """Inicia la unidad de trabajo creando sesión y repositorios."""
        self.session = self.db_manager.get_session()
        
        # Inicializar todos los repositorios
        self.pacientes = PacienteRepository(self.session)
        self.medicos = MedicoRepository(self.session)
        self.especialidades = EspecialidadRepository(self.session)
        self.estados_turno = EstadoTurnoRepository(self.session)
        self.turnos = TurnoRepository(self.session)
        self.disponibilidades = DisponibilidadMedicoRepository(self.session)
        self.bloqueos = BloqueoMedicoRepository(self.session)
        self.consultas = ConsultaRepository(self.session)
        self.recetas = RecetaRepository(self.session)
        self.items_receta = ItemRecetaRepository(self.session)
        self.recordatorios = RecordatorioRepository(self.session)
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Finaliza la unidad de trabajo.
        Hace rollback si hubo excepción, sino cierra la sesión.
        """
        if exc_type is not None:
            self.rollback()
        
        if self.session is not None:
            self.session.close()

    def commit(self) -> None:
        """Confirma todos los cambios en la BD."""
        if self.session is None:
            raise RuntimeError("No active session. Use within context manager.")
        
        try:
            self.session.commit()
        except Exception as e:
            self.rollback()
            raise e

    def rollback(self) -> None:
        """Revierte todos los cambios no confirmados."""
        if self.session is not None:
            self.session.rollback()

    def flush(self) -> None:
        """Envía los cambios a la BD sin hacer commit."""
        if self.session is not None:
            self.session.flush()

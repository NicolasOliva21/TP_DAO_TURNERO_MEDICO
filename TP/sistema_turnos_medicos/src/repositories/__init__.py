"""
Módulo de repositorios.
Exports para facilitar el acceso a los repositorios.
"""
from src.repositories.base_repository import BaseRepository
from src.repositories.consulta_repository import ConsultaRepository
from src.repositories.database import DatabaseManager, db_manager
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
from src.repositories.unit_of_work import UnitOfWork

__all__ = [
    # Database
    "DatabaseManager",
    "db_manager",
    # Base
    "BaseRepository",
    # Unit of Work
    "UnitOfWork",
    # Repositorios específicos
    "PacienteRepository",
    "MedicoRepository",
    "EspecialidadRepository",
    "EstadoTurnoRepository",
    "TurnoRepository",
    "DisponibilidadMedicoRepository",
    "BloqueoMedicoRepository",
    "ConsultaRepository",
    "RecetaRepository",
    "ItemRecetaRepository",
    "RecordatorioRepository",
]

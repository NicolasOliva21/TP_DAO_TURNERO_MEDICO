"""
Configuración base del sistema.
Implementa el patrón Singleton para la configuración global.
"""
from pathlib import Path
from typing import Optional


class Config:
    """Configuración del sistema (Singleton Pattern)."""
    
    _instance: Optional['Config'] = None
    
    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
            
        # Configuración de base de datos
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.DB_PATH = self.BASE_DIR / "data" / "turnos_medicos.db"
        self.DB_PATH.parent.mkdir(exist_ok=True)
        self.DATABASE_URL = f"sqlite:///{self.DB_PATH}"
        
        # Configuración de la aplicación
        self.APP_NAME = "Sistema de Gestión de Turnos Médicos"
        self.VERSION = "1.0.0"
        
        # Configuración de turnos
        self.DURACION_TURNO_DEFAULT = 30  # minutos
        self.ANTICIPACION_RECORDATORIO = 24  # horas
        
        self._initialized = True


# Instancia global de configuración
config = Config()

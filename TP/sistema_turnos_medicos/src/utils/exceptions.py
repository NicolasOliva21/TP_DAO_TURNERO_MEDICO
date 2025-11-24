"""
Excepciones personalizadas del sistema.
"""


class BusinessException(Exception):
    """Excepción base para errores de negocio."""
    pass


class EntityNotFoundException(BusinessException):
    """Excepción cuando no se encuentra una entidad."""
    
    def __init__(self, entity_type: str, identifier: str) -> None:
        self.entity_type = entity_type
        self.identifier = identifier
        super().__init__(f"{entity_type} no encontrado: {identifier}")


class DuplicateEntityException(BusinessException):
    """Excepción cuando se intenta crear una entidad duplicada."""
    
    def __init__(self, entity_type: str, field: str, value: str) -> None:
        self.entity_type = entity_type
        self.field = field
        self.value = value
        super().__init__(f"{entity_type} con {field}='{value}' ya existe")


class ValidationException(BusinessException):
    """Excepción para errores de validación."""
    
    def __init__(self, message: str) -> None:
        super().__init__(f"Error de validación: {message}")


class TurnoSolapamientoException(BusinessException):
    """Excepción cuando hay solapamiento de turnos."""
    
    def __init__(self, mensaje: str) -> None:
        super().__init__(f"Solapamiento de turnos: {mensaje}")


class DisponibilidadException(BusinessException):
    """Excepción cuando no hay disponibilidad."""
    
    def __init__(self, mensaje: str) -> None:
        super().__init__(f"No hay disponibilidad: {mensaje}")


class InvalidOperationException(BusinessException):
    """Excepción para operaciones inválidas."""
    
    def __init__(self, message: str) -> None:
        super().__init__(f"Operación inválida: {message}")


class TurnosPendientesException(BusinessException):
    """Excepción cuando hay turnos pendientes que impiden una operación."""
    
    def __init__(self, mensaje: str) -> None:
        super().__init__(f"Turnos pendientes: {mensaje}")

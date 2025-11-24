"""
Script principal del Sistema de Gestión de Turnos Médicos.
Inicia el servidor web con FastAPI y Uvicorn.
"""
import sys
import uvicorn
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    """Función principal que inicia el servidor web."""
    print("=" * 60)
    print("SISTEMA DE GESTIÓN DE TURNOS MÉDICOS")
    print("Universidad - Diseño y Arquitectura Orientada a Objetos")
    print("=" * 60)
    print()
    print("Iniciando servidor web...")
    print()
    print("Acceda a la aplicación en:")
    print("  → http://localhost:8000")
    print()
    print("Documentación de la API:")
    print("  → http://localhost:8000/api/docs")
    print("=" * 60)
    print()
    
    # Iniciar servidor Uvicorn
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Desactivado para evitar problemas con venv
        log_level="info"
    )


if __name__ == "__main__":
    main()

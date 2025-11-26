# Cómo ejecutar el Sistema de Turnos Médicos

## Prerrequisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## Instalación

1.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Linux/Mac:
    source venv/bin/activate
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

1.  **Iniciar el servidor:**
    Ejecuta el siguiente comando desde la raíz del proyecto:
    ```bash
    python main.py
    ```
    
    Esto iniciará:
    - La API REST en el puerto 8000.
    - El Frontend Web en `http://localhost:8000`. 
    - El planificador de recordatorios (Scheduler).
    - La base de datos (se creará automáticamente el archivo `turnos.db` y se cargarán datos de ejemplo).

## Uso del Sistema

1.  **Acceso al Frontend Web:**
    - Abre tu navegador en: [http://localhost:8000](http://localhost:8000)
    - Verás la página de inicio con estadísticas generales.

2.  **Documentación de API (Swagger UI):**
    - Abre: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
    - Aquí puedes probar todos los endpoints directamente.

3.  **Configuración de Email (Opcional):**
    Para que el envío de correos funcione realmente, configura las variables de entorno:
    - `SMTP_SERVER` (default: smtp.gmail.com)
    - `SMTP_PORT` (default: 587)
    - `SMTP_USER` (tu email)
    - `SMTP_PASSWORD` (tu contraseña de aplicación)

    En Windows (PowerShell):
    ```powershell
    $env:SMTP_USER="tucorreo@gmail.com"
    $env:SMTP_PASSWORD="tucontraseña"
    python main.py
    ```


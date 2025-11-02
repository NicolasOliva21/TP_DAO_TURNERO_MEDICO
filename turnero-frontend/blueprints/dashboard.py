from flask import Blueprint, render_template, session
import asyncio
from services.api import api

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.get("/")
def dashboard_view():
    token = session.get("token")
    # Ejemplo de pequeñas tarjetas con métricas (si el back las provee)
    try:
        resumen = asyncio.run(api.get("/reportes/resumen", token=token))
    except Exception:
        resumen = {"pacientes": 0, "medicos": 0, "turnos_hoy": 0}
    return render_template("dashboard.html", resumen=resumen)

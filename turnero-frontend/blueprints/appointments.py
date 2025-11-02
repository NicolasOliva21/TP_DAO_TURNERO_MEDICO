from flask import Blueprint, render_template, request, session, flash
import asyncio
from services.api import api

bp = Blueprint("appointments", __name__)

@bp.get("/")
def index():
    token = session.get("token")
    # cargar médicos para el selector
    try:
        medicos = asyncio.run(api.get("/medicos", token=token))
    except Exception as e:
        medicos = []
        flash(f"Error al cargar médicos: {e}", "error")
    return render_template("appointments/index.html", medicos=medicos)

# Partial de grilla de disponibilidad (HTMX)
@bp.get("/_grid")
def grid():
    token = session.get("token")
    medico_id = request.args.get("medico_id", type=int)
    fecha = request.args.get("fecha")
    dur = request.args.get("duracion_min", type=int, default=30)
    inicio = request.args.get("inicio", default="09:00")
    fin = request.args.get("fin", default="17:00")

    slots = []
    if medico_id and fecha:
        try:
            slots = asyncio.run(api.get("/turnos/disponibles",
                                        params={"medico_id": medico_id, "fecha": fecha,
                                                "duracion_min": dur, "inicio": inicio, "fin": fin},
                                        token=token))
        except Exception as e:
            flash(f"No se pudo obtener disponibilidad: {e}", "error")
    return render_template("appointments/_grid.html", slots=slots)

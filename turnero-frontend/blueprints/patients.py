from flask import Blueprint, render_template, request, session, flash
import asyncio
from services.api import api

bp = Blueprint("patients", __name__)

@bp.get("/")
def index():
    token = session.get("token")
    try:
        pacientes = asyncio.run(api.get("/pacientes", token=token))
    except Exception as e:
        pacientes = []
        flash(f"Error al cargar pacientes: {e}", "error")
    return render_template("patients/index.html", pacientes=pacientes)

# Fragmento de la tabla (HTMX)
@bp.get("/_table")
def table_partial():
    token = session.get("token")
    pacientes = asyncio.run(api.get("/pacientes", token=token))
    return render_template("patients/_table.html", pacientes=pacientes)

# Formulario de creación (HTMX)
@bp.get("/_form")
def form_partial():
    return render_template("patients/_form.html")

@bp.post("/crear")
def crear():
    token = session.get("token")
    payload = {
        "nombre": request.form.get("nombre", "").strip(),
        "apellido": request.form.get("apellido", "").strip(),
        "dni": request.form.get("dni", "").strip(),
        "fecha_nacimiento": request.form.get("fecha_nacimiento", ""),
        "direccion": request.form.get("direccion", ""),
        "telefono": request.form.get("telefono", ""),
        "email": request.form.get("email", ""),
        "obra_social": request.form.get("obra_social", "") or None,
        "nro_afiliado": request.form.get("nro_afiliado", "") or None
    }
    try:
        asyncio.run(api.post("/pacientes", payload, token=token))
        # Responder con la tabla actualizada para HTMX swap
        pacientes = asyncio.run(api.get("/pacientes", token=token))
        return render_template("patients/_table.html", pacientes=pacientes)
    except Exception as e:
        # Devolver el formulario con error inline
        return render_template("patients/_form.html", error=str(e), values=payload), 400

@bp.post("/toggle/<int:pid>")
def toggle(pid: int):
    token = session.get("token")
    activo = request.form.get("activo") == "true"
    try:
        asyncio.run(api.patch(f"/pacientes/{pid}/estado", {"activo": activo}, token=token))
        pacientes = asyncio.run(api.get("/pacientes", token=token))
        return render_template("patients/_table.html", pacientes=pacientes)
    except Exception as e:
        return f"Error: {e}", 400

from flask import Blueprint, render_template, session, request
import asyncio
from services.api import api

bp = Blueprint("doctors", __name__)

@bp.get("/")
def index():
    token = session.get("token")
    try:
        medicos = asyncio.run(api.get("/medicos", token=token))
    except Exception:
        medicos = []
    return render_template("doctors/index.html", medicos=medicos)

@bp.get("/_table")
def table_partial():
    token = session.get("token")
    medicos = asyncio.run(api.get("/medicos", token=token))
    return render_template("doctors/_table.html", medicos=medicos)

@bp.get("/_form")
def form_partial():
    return render_template("doctors/_form.html")

@bp.post("/crear")
def crear():
    token = session.get("token")
    payload = {
        "nombre": request.form.get("nombre","").strip(),
        "apellido": request.form.get("apellido","").strip(),
        "dni": request.form.get("dni","").strip(),
        "email": request.form.get("email") or None,
        "telefono": request.form.get("telefono") or None,
        "matricula": request.form.get("matricula","").strip(),
    }
    try:
        asyncio.run(api.post("/medicos", payload, token=token))
        medicos = asyncio.run(api.get("/medicos", token=token))
        return render_template("doctors/_table.html", medicos=medicos)
    except Exception as e:
        return render_template("doctors/_form.html", error=str(e), values=payload), 400

@bp.post("/toggle/<int:did>")
def toggle(did: int):
    token = session.get("token")
    activo = request.form.get("activo") == "true"
    try:
        asyncio.run(api.patch(f"/medicos/{did}/estado", {"activo": activo}, token=token))
        medicos = asyncio.run(api.get("/medicos", token=token))
        return render_template("doctors/_table.html", medicos=medicos)
    except Exception as e:
        return f"Error: {e}", 400

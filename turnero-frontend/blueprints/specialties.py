from flask import Blueprint, render_template, session
import asyncio
from services.api import api

bp = Blueprint("specialties", __name__)

@bp.get("/")
def index():
    token = session.get("token")
    try:
        especialidades = asyncio.run(api.get("/especialidades", token=token))
    except Exception:
        especialidades = []
    return render_template("specialties/index.html", especialidades=especialidades)

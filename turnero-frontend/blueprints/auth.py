from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import asyncio
from services.api import api

bp = Blueprint("auth", __name__)

@bp.get("/login")
def login_view():
    return render_template("login.html")

@bp.post("/login")
def login_post():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    try:
        data = asyncio.run(api.post("/auth/login", {"email": email, "password": password}))
        session["token"] = data["token"]
        session["user"] = data["user"]
        return redirect(url_for("dashboard.dashboard_view"))
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("auth.login_view"))

@bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_view"))

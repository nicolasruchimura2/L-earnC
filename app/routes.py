from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from . import db
from .models import User

auth_bp = Blueprint("auth", __name__)
main_bp = Blueprint("main", __name__)

COURSE_PARTS = [
    {
        "id": idx,
        "title": f"Part {idx}",
        "description": "Placeholder description — update soon.",
    }
    for idx in range(1, 9)
]


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not email or not password:
            flash("Email and password are required.", "danger")
        elif password != confirm:
            flash("Passwords do not match.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Email already registered.", "warning")
        else:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Welcome back!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.dashboard"))

        flash("Invalid credentials.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Signed out successfully.", "info")
    return redirect(url_for("auth.login"))


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user, parts=COURSE_PARTS)


@main_bp.route("/parts/<int:part_id>")
@login_required
def part_detail(part_id: int):
    part = next((p for p in COURSE_PARTS if p["id"] == part_id), None)
    if not part:
        abort(404)
    return render_template("part_detail.html", part=part)


@main_bp.route("/parts/<int:part_id>/start", methods=["POST"])
@login_required
def start_part(part_id: int):
    part = next((p for p in COURSE_PARTS if p["id"] == part_id), None)
    if not part:
        abort(404)
    flash(f"{part['title']} kicked off. Feel free to explore other parts anytime.", "success")
    return redirect(url_for("main.dashboard"))


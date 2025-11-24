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

# ============================================================================
# COURSE PARTS CONFIGURATION
# ============================================================================
# Each part can be personalized with unique titles and descriptions.
# Each part contains 10 classes - customize them individually below.
# ============================================================================

def create_classes(part_id, class_titles=None, class_descriptions=None):
    """Helper function to create 10 classes for a part with optional customization."""
    classes = []
    for class_idx in range(1, 11):
        title = class_titles[class_idx - 1] if class_titles and len(class_titles) > class_idx - 1 else f"Class {class_idx:02d}"
        desc = class_descriptions[class_idx - 1] if class_descriptions and len(class_descriptions) > class_idx - 1 else f"Learn essential concepts in Part {part_id}, Class {class_idx:02d}."
        classes.append({
            "id": class_idx,
            "title": title,
            "description": desc,
        })
    return classes

COURSE_PARTS = [
    {
        "id": 1,
        "title": "Part 1: Fundamentals",
        "description": "Begin your C programming journey! Learn the fundamentals, syntax basics, and write your first programs. Perfect for absolute beginners.",
        "classes": create_classes(1),
    },
    {
        "id": 2,
        "title": "Part 2: Variables & Data Types",
        "description": "Master variables, constants, and data types in C. Understand memory allocation, type casting, and how to work with different numeric and character types.",
        "classes": create_classes(2),
    },
    {
        "id": 3,
        "title": "Part 3: Control Flow",
        "description": "Learn conditional statements, loops, and program flow control. Master if-else, switch, for, while, and do-while loops to build dynamic programs.",
        "classes": create_classes(3),
    },
    {
        "id": 4,
        "title": "Part 4: Functions & Scope",
        "description": "Dive into functions, parameters, return values, and variable scope. Learn to write reusable, modular code and understand recursion.",
        "classes": create_classes(4),
    },
    {
        "id": 5,
        "title": "Part 5: Arrays & Strings",
        "description": "Work with arrays, multidimensional arrays, and string manipulation. Learn essential algorithms for searching, sorting, and string operations.",
        "classes": create_classes(5),
    },
    {
        "id": 6,
        "title": "Part 6: Pointers & Memory",
        "description": "Master pointers, memory addresses, and dynamic memory allocation. Understand the power and pitfalls of pointer arithmetic and memory management.",
        "classes": create_classes(6),
    },
    {
        "id": 7,
        "title": "Part 7: Structures & Unions",
        "description": "Learn to create custom data types with structures and unions. Organize complex data and build more sophisticated programs.",
        "classes": create_classes(7),
    },
    {
        "id": 8,
        "title": "Part 8: Advanced Topics",
        "description": "Explore file I/O, preprocessor directives, error handling, and advanced C features. Prepare for real-world programming challenges.",
        "classes": create_classes(8),
    },
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


import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "aceest-development-key")

DATABASE = os.environ.get(
    "FITNESS_DATABASE",
    os.path.join(app.root_path, "instance", "fitness.db"),
)


def get_db():
    os.makedirs(os.path.dirname(os.path.abspath(DATABASE)), exist_ok=True)
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with get_db() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL CHECK(age > 0),
                height REAL NOT NULL CHECK(height > 0),
                weight REAL NOT NULL CHECK(weight > 0),
                membership TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                workout TEXT NOT NULL,
                duration INTEGER NOT NULL CHECK(duration > 0),
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                FOREIGN KEY(member_id) REFERENCES members(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS weight_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                weight REAL NOT NULL CHECK(weight > 0),
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                FOREIGN KEY(member_id) REFERENCES members(id)
                    ON DELETE CASCADE
            );
            """
        )


@app.route("/")
def dashboard():
    with get_db() as db:
        members = db.execute(
            "SELECT * FROM members ORDER BY id DESC"
        ).fetchall()
        workouts = db.execute(
            """
            SELECT workouts.*, members.name AS member_name
            FROM workouts
            JOIN members ON members.id = workouts.member_id
            ORDER BY workouts.id DESC LIMIT 10
            """
        ).fetchall()

        total_members = db.execute(
            "SELECT COUNT(*) FROM members"
        ).fetchone()[0]
        total_workouts = db.execute(
            "SELECT COUNT(*) FROM workouts"
        ).fetchone()[0]

    return render_template(
        "dashboard.html",
        members=members,
        workouts=workouts,
        total_members=total_members,
        total_workouts=total_workouts,
    )


@app.route("/clients", methods=["POST"])
def add_member():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    membership = request.form.get("membership", "Monthly")
    allowed_memberships = {
        "Monthly", "Quarterly", "Annual", "Expired"
    }

    try:
        age = int(request.form.get("age", ""))
        height = float(request.form.get("height", ""))
        weight = float(request.form.get("weight", ""))

        if (
            not name
            or not email
            or age <= 0
            or height <= 0
            or weight <= 0
            or membership not in allowed_memberships
        ):
            raise ValueError

        with get_db() as db:
            cursor = db.execute(
                """
                INSERT INTO members
                (name, email, age, height, weight, membership, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    age,
                    height,
                    weight,
                    membership,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            member_id = cursor.lastrowid
            db.execute(
                """
                INSERT INTO weight_history
                (member_id, weight, notes, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    member_id,
                    weight,
                    "Initial measurement",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
        flash("Member registered successfully.", "success")
    except ValueError:
        flash("Enter valid member details.", "error")
    except sqlite3.IntegrityError:
        flash("This email address is already registered.", "error")

    return redirect(url_for("dashboard"))


@app.route("/clients/<int:client_id>")
def member_profile(client_id):
    with get_db() as db:
        member = db.execute(
            "SELECT * FROM members WHERE id = ?", (client_id,)
        ).fetchone()

        if member is None:
            return "Member not found", 404

        workouts = db.execute(
            """
            SELECT * FROM workouts
            WHERE member_id = ? ORDER BY id DESC
            """,
            (client_id,),
        ).fetchall()
        weights = db.execute(
            """
            SELECT * FROM weight_history
            WHERE member_id = ? ORDER BY id DESC
            """,
            (client_id,),
        ).fetchall()

    bmi = member["weight"] / ((member["height"] / 100) ** 2)
    return render_template(
        "client.html",
        member=member,
        workouts=workouts,
        weights=weights,
        bmi=round(bmi, 1),
    )


@app.route("/clients/<int:client_id>/metrics", methods=["POST"])
def add_weight(client_id):
    try:
        weight = float(request.form.get("weight", ""))
        notes = request.form.get("notes", "").strip()
        if weight <= 0:
            raise ValueError

        with get_db() as db:
            member = db.execute(
                "SELECT id FROM members WHERE id = ?", (client_id,)
            ).fetchone()
            if member is None:
                return "Member not found", 404

            db.execute(
                """
                INSERT INTO weight_history
                (member_id, weight, notes, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    client_id,
                    weight,
                    notes,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            db.execute(
                "UPDATE members SET weight = ? WHERE id = ?",
                (weight, client_id),
            )
        flash("Weight measurement saved.", "success")
    except ValueError:
        flash("Enter a valid weight.", "error")

    return redirect(url_for("member_profile", client_id=client_id))


@app.route("/workouts", methods=["POST"])
def add_workout():
    try:
        member_id = int(request.form.get("member_id", ""))
        workout = request.form.get("workout", "").strip()
        duration = int(request.form.get("duration", ""))
        notes = request.form.get("notes", "").strip()

        if not workout or duration <= 0:
            raise ValueError

        with get_db() as db:
            member = db.execute(
                "SELECT id FROM members WHERE id = ?", (member_id,)
            ).fetchone()
            if member is None:
                flash("Select a valid member first.", "error")
                return redirect(url_for("dashboard"))

            db.execute(
                """
                INSERT INTO workouts
                (member_id, workout, duration, notes, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    member_id,
                    workout,
                    duration,
                    notes,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
        flash("Workout recorded successfully.", "success")
    except ValueError:
        flash("Enter a valid workout and duration.", "error")

    return redirect(url_for("dashboard"))


@app.route("/clients/<int:client_id>/delete", methods=["POST"])
def delete_member(client_id):
    with get_db() as db:
        db.execute("DELETE FROM members WHERE id = ?", (client_id,))
    flash("Member deleted.", "success")
    return redirect(url_for("dashboard"))


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

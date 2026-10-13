import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import app as fitness_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    database = tmp_path / "test_fitness.db"
    monkeypatch.setattr(fitness_app, "DATABASE", str(database))
    fitness_app.init_db()
    fitness_app.app.config["TESTING"] = True

    with fitness_app.app.test_client() as test_client:
        yield test_client


def register_member(client, email="test@example.com"):
    return client.post(
        "/clients",
        data={
            "name": "Test Member",
            "email": email,
            "age": "25",
            "height": "175",
            "weight": "70",
            "membership": "Monthly",
        },
        follow_redirects=True,
    )


def test_dashboard_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Register Member" in response.data
    assert b"Record Workout" in response.data


def test_register_member(client):
    response = register_member(client)
    assert response.status_code == 200
    assert b"Member registered successfully." in response.data
    assert b"Test Member" in response.data


def test_duplicate_email_is_rejected(client):
    register_member(client)
    response = register_member(client)
    assert b"already registered" in response.data


def test_invalid_member_is_rejected(client):
    response = client.post(
        "/clients",
        data={
            "name": "",
            "email": "invalid@example.com",
            "age": "0",
            "height": "175",
            "weight": "70",
            "membership": "Monthly",
        },
        follow_redirects=True,
    )
    assert b"Enter valid member details." in response.data


def test_member_profile_and_bmi(client):
    register_member(client)
    response = client.get("/clients/1")
    assert response.status_code == 200
    assert b"Test Member" in response.data
    assert b"22.9" in response.data


def test_unknown_member_returns_404(client):
    response = client.get("/clients/999")
    assert response.status_code == 404


def test_record_workout(client):
    register_member(client)
    response = client.post(
        "/workouts",
        data={
            "member_id": "1",
            "workout": "Strength training",
            "duration": "30",
            "notes": "Test session",
        },
        follow_redirects=True,
    )
    assert b"Workout recorded successfully." in response.data
    assert b"Strength training" in response.data


def test_record_weight_measurement(client):
    register_member(client)
    response = client.post(
        "/clients/1/metrics",
        data={"weight": "68.5", "notes": "Test measurement"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    with fitness_app.get_db() as db:
        member = db.execute(
            "SELECT weight FROM members WHERE id = ?", (1,)
        ).fetchone()
        measurement = db.execute(
            """
            SELECT weight, notes FROM weight_history
            WHERE member_id = ? AND notes = ?
            """,
            (1, "Test measurement"),
        ).fetchone()

    assert member["weight"] == 68.5
    assert measurement is not None
    assert measurement["weight"] == 68.5


def test_delete_member(client):
    register_member(client)
    response = client.post(
        "/clients/1/delete",
        follow_redirects=True,
    )
    assert b"Member deleted." in response.data
    assert b"Test Member" not in response.data

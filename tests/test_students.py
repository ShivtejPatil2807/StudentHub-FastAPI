
def test_create_student(client):

    response = client.post(
        "/students",
        json={
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
            "course": "Computer Science"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Student added successfully"
    assert data["student"]["name"] == "Rahul Sharma"


def test_get_all_students(client):

    client.post(
        "/students",
        json={
            "name": "Priya",
            "email": "priya@example.com",
            "course": "Information Technology"
        }
    )

    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Priya"


def test_get_student_by_id(client):

    create_response = client.post(
        "/students",
        json={
            "name": "Amit",
            "email": "amit@example.com",
            "course": "Artificial Intelligence"
        }
    )

    student_id = create_response.json()["student"]["id"]

    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Amit"


def test_search_students(client):

    client.post(
        "/students",
        json={
            "name": "Rahul",
            "email": "rahul@example.com",
            "course": "Computer Science"
        }
    )

    response = client.get("/students/search?name=Rahul")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_student(client):

    create_response = client.post(
        "/students",
        json={
            "name": "Rahul",
            "email": "rahul@example.com",
            "course": "Computer Science"
        }
    )

    student_id = create_response.json()["student"]["id"]

    response = client.put(
        f"/students/{student_id}",
        json={
            "name": "Rahul Updated",
            "email": "rahul@example.com",
            "course": "Artificial Intelligence"
        }
    )

    assert response.status_code == 200
    assert response.json()["student"]["name"] == "Rahul Updated"


def test_delete_student(client):

    create_response = client.post(
        "/students",
        json={
            "name": "Rahul",
            "email": "rahul@example.com",
            "course": "Computer Science"
        }
    )

    student_id = create_response.json()["student"]["id"]

    response = client.delete(f"/students/{student_id}")

    assert response.status_code == 200

    get_response = client.get(f"/students/{student_id}")

    assert get_response.status_code == 404


def test_invalid_student_email(client):

    response = client.post(
        "/students",
        json={
            "name": "Rahul",
            "email": "invalid-email",
            "course": "Computer Science"
        }
    )

    assert response.status_code == 422


def test_duplicate_student_email(client):

    student = {
        "name": "Rahul",
        "email": "rahul@example.com",
        "course": "Computer Science"
    }

    first_response = client.post("/students", json=student)
    second_response = client.post("/students", json=student)

    assert first_response.status_code == 201
    assert second_response.status_code == 409

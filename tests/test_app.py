from src.app import activities


def test_root_redirects_to_static(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_list(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == activities


def test_signup_for_activity_success(client):
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_for_activity_fails_when_activity_not_found(client):
    response = client.post(
        "/activities/Nonexistent/signup",
        params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_fails_when_student_already_signed_up(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_for_activity_fails_when_activity_is_full(client):
    activity_name = "Basketball Team"
    activities[activity_name]["max_participants"] = 1
    activities[activity_name]["participants"].append("existing@mergington.edu")

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "newstudent@mergington.edu"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unregister_from_activity_success(client):
    activity_name = "Programming Class"
    email = "student@mergington.edu"
    activities[activity_name]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_from_activity_fails_when_activity_not_found(client):
    response = client.delete(
        "/activities/Nonexistent/unregister",
        params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_fails_when_student_not_registered(client):
    activity_name = "Science Club"

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"

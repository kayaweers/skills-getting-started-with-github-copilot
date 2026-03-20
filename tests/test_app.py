def test_given_valid_activity_when_get_activities_then_return_activities(client):
    # Given: a running FastAPI TestClient and existing activities
    # When: GET /activities
    response = client.get("/activities")

    # Then: status 200 and includes Chess Club activity
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload


def test_given_new_email_when_signup_for_activity_then_success(client):
    # Given: activity exists and email is not yet signed up
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # When: POST signup with email query param
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Then: status 200 and participant is added
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_given_already_signed_up_email_when_signup_for_activity_then_bad_request(client):
    # Given: email already signed up for activity
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # When: POST signup with duplicate email
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Then: status 400 with correct error detail
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_given_invalid_activity_when_signup_then_not_found(client):
    # Given: non-existent activity name
    activity_name = "Nonexistent Club"
    email = "foo@bar.com"

    # When: POST signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Then: status 404
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_given_signed_up_email_when_unregister_then_success(client):
    # Given: signed-up email in activity
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # When: POST unregister
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Then: status 200 and email removed
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_given_unregistered_email_when_unregister_then_bad_request(client):
    # Given: email not signed up
    activity_name = "Chess Club"
    email = "notinsignup@mergington.edu"

    # When: POST unregister
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Then: status 400
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_given_invalid_activity_when_unregister_then_not_found(client):
    # Given: non-existent activity
    activity_name = "Nonexistent Club"
    email = "foo@bar.com"

    # When: POST unregister
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Then: status 404
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

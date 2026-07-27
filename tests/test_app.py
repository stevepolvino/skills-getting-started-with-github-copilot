def test_unregister_participant_removes_user_from_activity(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert unregister_response.status_code == 200

    payload = unregister_response.json()
    assert "removed" in payload["message"].lower()

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_activities_endpoint_is_not_cached(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert "no-store" in response.headers.get("cache-control", "")

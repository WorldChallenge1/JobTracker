# features/steps/common_steps.py
"""
Shared step definitions for the Job Tracker BDD suite.
All steps are written against a running FastAPI test server using
the `requests` library and a clean SQLite / PostgreSQL test DB.

Usage:
    behave features/applications.feature
    behave features/interviews.feature
    behave features/application_status.feature
"""

import json
import requests
from behave import given, when, then

BASE_URL = "http://localhost:8000"


# ---------------------------------------------------------------------------
# Background / setup
# ---------------------------------------------------------------------------

@given("the database is clean")
def step_db_clean(context):
    """Call a test-only teardown endpoint or truncate tables directly."""
    requests.post(f"{BASE_URL}/test/reset")


@given("the API is running")
def step_api_running(context):
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200, "API is not running"


# ---------------------------------------------------------------------------
# Application fixtures
# ---------------------------------------------------------------------------

@given("an application exists with:")
def step_application_exists(context):
    payload = {row["field"]: row["value"] for row in context.table}
    response = requests.post(f"{BASE_URL}/applications", json=payload)
    assert response.status_code == 201, response.text
    context.application = response.json()
    context.application_id = context.application["id"]


@given('an application exists with status "{status}"')
def step_application_exists_with_status(context, status):
    payload = {"position": "Engineer", "company": "Acme", "status": status}
    response = requests.post(f"{BASE_URL}/applications", json=payload)
    assert response.status_code == 201, response.text
    context.application = response.json()
    context.application_id = context.application["id"]


@given("the following applications exist:")
def step_multiple_applications_exist(context):
    context.applications = []
    for row in context.table:
        payload = {heading: row[heading] for heading in row.headings}
        response = requests.post(f"{BASE_URL}/applications", json=payload)
        assert response.status_code == 201, response.text
        context.applications.append(response.json())


@given("a second application exists")
def step_second_application_exists(context):
    payload = {"position": "Designer", "company": "Beta", "status": "Applied"}
    response = requests.post(f"{BASE_URL}/applications", json=payload)
    assert response.status_code == 201, response.text
    context.second_application = response.json()
    context.second_application_id = context.second_application["id"]


# ---------------------------------------------------------------------------
# Interview fixtures
# ---------------------------------------------------------------------------

@given("an interview exists for the application with:")
def step_interview_exists(context):
    payload = {row["field"]: row["value"] for row in context.table}
    app_id = context.application_id
    response = requests.post(
        f"{BASE_URL}/applications/{app_id}/interviews", json=payload
    )
    assert response.status_code == 201, response.text
    context.interview = response.json()
    context.interview_id = context.interview["id"]


@given("an interview exists for the second application with:")
def step_interview_exists_second_app(context):
    payload = {row["field"]: row["value"] for row in context.table}
    app_id = context.second_application_id
    response = requests.post(
        f"{BASE_URL}/applications/{app_id}/interviews", json=payload
    )
    assert response.status_code == 201, response.text
    context.second_interview = response.json()
    context.second_interview_id = context.second_interview["id"]


@given("the following interviews exist for the application:")
def step_multiple_interviews_exist(context):
    context.interviews = []
    app_id = context.application_id
    for row in context.table:
        payload = {heading: row[heading] for heading in row.headings}
        response = requests.post(
            f"{BASE_URL}/applications/{app_id}/interviews", json=payload
        )
        assert response.status_code == 201, response.text
        context.interviews.append(response.json())


# ---------------------------------------------------------------------------
# HTTP actions — generic helpers
# ---------------------------------------------------------------------------

def _resolve_url(context, url_template):
    """Replace {id}, {application_id}, etc. with stored context values."""
    url = url_template
    if "{id}" in url:
        resource_id = getattr(context, "interview_id", None) or context.application_id
        url = url.replace("{id}", str(resource_id))
    if "{application_id}" in url:
        url = url.replace("{application_id}", str(context.application_id))
    if "{second_interview_id}" in url:
        url = url.replace("{second_interview_id}", str(context.second_interview_id))
    return BASE_URL + url


@when('I send a GET request to "{url_template}"')
def step_get(context, url_template):
    context.response = requests.get(_resolve_url(context, url_template))


@when('I send a POST request to "{url_template}" with body:')
def step_post(context, url_template):
    payload = json.loads(context.text)
    context.response = requests.post(
        _resolve_url(context, url_template), json=payload
    )


@when('I send a PATCH request to "{url_template}" with body:')
def step_patch(context, url_template):
    payload = json.loads(context.text)
    context.response = requests.patch(
        _resolve_url(context, url_template), json=payload
    )


@when('I send a DELETE request to "{url_template}"')
def step_delete(context, url_template):
    context.response = requests.delete(_resolve_url(context, url_template))


# ---------------------------------------------------------------------------
# Assertions — status codes
# ---------------------------------------------------------------------------

@then("the response status code should be {expected_code:d}")
def step_status_code(context, expected_code):
    actual = context.response.status_code
    assert actual == expected_code, (
        f"Expected {expected_code}, got {actual}. Body: {context.response.text}"
    )


# ---------------------------------------------------------------------------
# Assertions — body content
# ---------------------------------------------------------------------------

@then("the response body should contain:")
def step_body_contains_table(context):
    body = context.response.json()
    if isinstance(body, dict):
        for row in context.table:
            field, expected = row["field"], row["value"]
            actual = body.get(field)
            assert str(actual) == str(expected), (
                f"Field '{field}': expected '{expected}', got '{actual}'"
            )
    elif isinstance(body, list):
        headings = context.table.headings
        for row in context.table:
            expected = {heading: row[heading] for heading in headings}
            assert any(
                all(str(item.get(k)) == str(v) for k, v in expected.items())
                for item in body
            ), f"Response does not contain entry matching {expected}"


@then('the response body field "{field}" should equal "{expected}"')
def step_body_field_equals(context, field, expected):
    body = context.response.json()
    actual = body.get(field)
    assert str(actual) == expected, (
        f"Field '{field}': expected '{expected}', got '{actual}'"
    )


@then('the response body should include a generated "{field}"')
def step_body_has_generated_field(context, field):
    body = context.response.json()
    assert field in body and body[field] is not None, (
        f"Expected generated field '{field}' in response body"
    )


@then('the response body field "application_id" should match the parent application')
def step_interview_application_id_matches(context):
    body = context.response.json()
    assert body.get("application_id") == context.application_id, (
        f"application_id mismatch: {body.get('application_id')} != {context.application_id}"
    )


@then('the response body should contain a validation error for field "{field}"')
def step_validation_error(context, field):
    body = context.response.json()
    errors = body.get("detail", [])
    assert any(field in str(err) for err in errors), (
        f"Expected validation error for '{field}' in: {body}"
    )


@then("the response body should be an empty list")
def step_empty_list(context):
    body = context.response.json()
    assert body == [], f"Expected empty list, got: {body}"


@then("the response body should be a list of {count:d} applications")
def step_list_of_n_applications(context, count):
    body = context.response.json()
    assert isinstance(body, list), f"Expected list, got {type(body)}"
    assert len(body) == count, f"Expected {count} items, got {len(body)}"


@then("the response body should be a list of {count:d} interviews")
def step_list_of_n_interviews(context, count):
    body = context.response.json()
    assert isinstance(body, list), f"Expected list, got {type(body)}"
    assert len(body) == count, f"Expected {count} items, got {len(body)}"


@then('every application in the list should have status "{expected_status}"')
def step_every_app_status(context, expected_status):
    body = context.response.json()
    for app in body:
        assert app["status"] == expected_status, (
            f"Found application with status '{app['status']}'"
        )


@then('every application in the list should have company "{expected_company}"')
def step_every_app_company(context, expected_company):
    body = context.response.json()
    for app in body:
        assert app["company"] == expected_company, (
            f"Found application with company '{app['company']}'"
        )


@then("every status in the summary should have count 0")
def step_summary_all_zero(context):
    body = context.response.json()
    for entry in body:
        assert entry["count"] == 0, (
            f"Status '{entry['status']}' has count {entry['count']}, expected 0"
        )


# ---------------------------------------------------------------------------
# Assertions — cascading / follow-up requests
# ---------------------------------------------------------------------------

@then('a subsequent GET request to "{url_template}" should return {expected_code:d}')
def step_followup_get(context, url_template, expected_code):
    response = requests.get(_resolve_url(context, url_template))
    assert response.status_code == expected_code, (
        f"Expected {expected_code}, got {response.status_code}"
    )

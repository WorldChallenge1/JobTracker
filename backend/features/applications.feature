# features/applications.feature

Feature: Job Application Management
  As a job seeker
  I want to manage my job applications
  So that I can track my job search progress

  Background:
    Given the database is clean
    And the API is running

  # ---------------------------------------------------------------------------
  # CREATE
  # ---------------------------------------------------------------------------

  Scenario: Successfully create a job application with all fields
    When I send a POST request to "/applications" with body:
      """
      {
        "position": "Full Stack Developer (Python)",
        "company": "Perform",
        "status": "Applied",
        "cv": "CV_2025_v3_Senior.pdf",
        "applied_date": "2025-04-10",
        "location": "Remote",
        "salary": "$180k–$220k",
        "applied_through": "LinkedIn",
        "notes": "Applied via referral from @tomas."
      }
      """
    Then the response status code should be 201
    And the response body should contain:
      | field          | value                          |
      | position       | Full Stack Developer (Python)  |
      | company        | Perform                        |
      | status         | Applied                        |
      | cv             | CV_2025_v3_Senior.pdf          |
      | applied_date   | 2025-04-10                     |
      | location       | Remote                         |
      | salary         | $180k–$220k                    |
      | applied_through| LinkedIn                       |
      | notes          | Applied via referral from @tomas. |
    And the response body should include a generated "id"
    And the response body should include a generated "created_at"

  Scenario: Successfully create a job application with only required fields
    When I send a POST request to "/applications" with body:
      """
      {
        "position": "Backend Engineer",
        "company": "Acme Corp",
        "status": "Applied"
      }
      """
    Then the response status code should be 201
    And the response body field "position" should equal "Backend Engineer"
    And the response body field "company" should equal "Acme Corp"
    And the response body field "status" should equal "Applied"
    And the response body should include a generated "id"

  Scenario Outline: Successfully create an application with each valid status
    When I send a POST request to "/applications" with body:
      """
      {
        "position": "Engineer",
        "company": "TechCorp",
        "status": "<status>"
      }
      """
    Then the response status code should be 201
    And the response body field "status" should equal "<status>"

    Examples:
      | status       |
      | Applied      |
      | Interviewing |
      | Offer        |
      | Accepted     |
      | Rejected     |
      | Ghosted      |

  Scenario: Fail to create an application when required fields are missing
    When I send a POST request to "/applications" with body:
      """
      {
        "company": "Acme Corp",
        "status": "Applied"
      }
      """
    Then the response status code should be 422
    And the response body should contain a validation error for field "position"

  Scenario: Fail to create an application with an invalid status
    When I send a POST request to "/applications" with body:
      """
      {
        "position": "Backend Engineer",
        "company": "Acme Corp",
        "status": "Pending"
      }
      """
    Then the response status code should be 422
    And the response body should contain a validation error for field "status"

  Scenario: Fail to create an application with an invalid applied_date format
    When I send a POST request to "/applications" with body:
      """
      {
        "position": "Backend Engineer",
        "company": "Acme Corp",
        "status": "Applied",
        "applied_date": "10-04-2025"
      }
      """
    Then the response status code should be 422
    And the response body should contain a validation error for field "applied_date"

  # ---------------------------------------------------------------------------
  # READ — single
  # ---------------------------------------------------------------------------

  Scenario: Successfully retrieve an existing application by ID
    Given an application exists with:
      | field    | value            |
      | position | DevOps Engineer  |
      | company  | CloudBase        |
      | status   | Applied          |
    When I send a GET request to "/applications/{id}"
    Then the response status code should be 200
    And the response body field "position" should equal "DevOps Engineer"
    And the response body field "company" should equal "CloudBase"

  Scenario: Fail to retrieve an application that does not exist
    When I send a GET request to "/applications/99999"
    Then the response status code should be 404
    And the response body field "detail" should equal "Application not found"

  # ---------------------------------------------------------------------------
  # READ — list
  # ---------------------------------------------------------------------------

  Scenario: Successfully retrieve a list of all applications
    Given the following applications exist:
      | position              | company    | status   |
      | Frontend Developer    | PixelWorks | Applied  |
      | Backend Engineer      | DataFlow   | Rejected |
      | Full Stack Developer  | Perform    | Offer    |
    When I send a GET request to "/applications"
    Then the response status code should be 200
    And the response body should be a list of 3 applications

  Scenario: Retrieve an empty list when no applications exist
    When I send a GET request to "/applications"
    Then the response status code should be 200
    And the response body should be an empty list

  Scenario: Filter applications by status
    Given the following applications exist:
      | position           | company  | status       |
      | Frontend Developer | Acme     | Applied      |
      | Backend Engineer   | Beta     | Interviewing |
      | Data Scientist     | Gamma    | Applied      |
    When I send a GET request to "/applications?status=Applied"
    Then the response status code should be 200
    And the response body should be a list of 2 applications
    And every application in the list should have status "Applied"

  Scenario: Filter applications by company
    Given the following applications exist:
      | position        | company | status  |
      | Engineer        | Perform | Applied |
      | Designer        | Perform | Ghosted |
      | Product Manager | Acme    | Applied |
    When I send a GET request to "/applications?company=Perform"
    Then the response status code should be 200
    And the response body should be a list of 2 applications
    And every application in the list should have company "Perform"

  Scenario: Filter applications by location
    Given the following applications exist:
      | position   | company | status  | location |
      | Engineer   | Acme    | Applied | Remote   |
      | Designer   | Beta    | Applied | On-site  |
      | QA Analyst | Gamma   | Applied | Remote   |
    When I send a GET request to "/applications?location=Remote"
    Then the response status code should be 200
    And the response body should be a list of 2 applications

  # ---------------------------------------------------------------------------
  # UPDATE
  # ---------------------------------------------------------------------------

  Scenario: Successfully update an application's status
    Given an application exists with:
      | field    | value           |
      | position | Backend Engineer|
      | company  | DataFlow        |
      | status   | Applied         |
    When I send a PATCH request to "/applications/{id}" with body:
      """
      {
        "status": "Interviewing"
      }
      """
    Then the response status code should be 200
    And the response body field "status" should equal "Interviewing"

  Scenario: Successfully update multiple fields of an application
    Given an application exists with:
      | field    | value           |
      | position | Backend Engineer|
      | company  | DataFlow        |
      | status   | Applied         |
    When I send a PATCH request to "/applications/{id}" with body:
      """
      {
        "salary": "$120k–$140k",
        "notes": "Recruiter reached out.",
        "location": "Hybrid"
      }
      """
    Then the response status code should be 200
    And the response body field "salary" should equal "$120k–$140k"
    And the response body field "notes" should equal "Recruiter reached out."
    And the response body field "location" should equal "Hybrid"

  Scenario: Fail to update an application that does not exist
    When I send a PATCH request to "/applications/99999" with body:
      """
      {
        "status": "Rejected"
      }
      """
    Then the response status code should be 404
    And the response body field "detail" should equal "Application not found"

  Scenario: Fail to update an application with an invalid status
    Given an application exists with:
      | field    | value   |
      | position | Engineer|
      | company  | Acme    |
      | status   | Applied |
    When I send a PATCH request to "/applications/{id}" with body:
      """
      {
        "status": "Cancelled"
      }
      """
    Then the response status code should be 422
    And the response body should contain a validation error for field "status"

  # ---------------------------------------------------------------------------
  # DELETE
  # ---------------------------------------------------------------------------

  Scenario: Successfully delete an existing application
    Given an application exists with:
      | field    | value   |
      | position | Engineer|
      | company  | Acme    |
      | status   | Applied |
    When I send a DELETE request to "/applications/{id}"
    Then the response status code should be 204
    And a subsequent GET request to "/applications/{id}" should return 404

  Scenario: Fail to delete an application that does not exist
    When I send a DELETE request to "/applications/99999"
    Then the response status code should be 404
    And the response body field "detail" should equal "Application not found"

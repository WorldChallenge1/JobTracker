# features/interviews.feature

Feature: Interview Management
  As a job seeker
  I want to manage interviews linked to my job applications
  So that I can stay prepared and organised throughout my hiring process

  Background:
    Given the database is clean
    And the API is running
    And an application exists with:
      | field    | value                         |
      | position | Full Stack Developer (Python) |
      | company  | Perform                       |
      | status   | Interviewing                  |

  # ---------------------------------------------------------------------------
  # CREATE
  # ---------------------------------------------------------------------------

  Scenario: Successfully create an interview with all fields
    When I send a POST request to "/applications/{application_id}/interviews" with body:
      """
      {
        "date": "2025-05-14",
        "time": "14:00",
        "type": "Technical",
        "notes": "System design focus",
        "interviewer": "Alex Park"
      }
      """
    Then the response status code should be 201
    And the response body should contain:
      | field        | value               |
      | date         | 2025-05-14          |
      | time         | 14:00               |
      | type         | Technical           |
      | notes        | System design focus |
      | interviewer  | Alex Park           |
    And the response body should include a generated "id"
    And the response body field "application_id" should match the parent application

  Scenario: Successfully create an interview with only required fields
    When I send a POST request to "/applications/{application_id}/interviews" with body:
      """
      {
        "date": "2025-05-20",
        "time": "10:00",
        "type": "HR Interview"
      }
      """
    Then the response status code should be 201
    And the response body field "date" should equal "2025-05-20"
    And the response body field "type" should equal "HR Interview"
    And the response body should include a generated "id"

  Scenario Outline: Successfully create an interview with each valid type
    When I send a POST request to "/applications/{application_id}/interviews" with body:
      """
      {
        "date": "2025-06-01",
        "time": "09:00",
        "type": "<type>"
      }
      """
    Then the response status code should be 201
    And the response body field "type" should equal "<type>"

    Examples:
      | type          |
      | Phone Screen  |
      | HR Interview  |
      | Technical     |
      | System Design |
      | Behavioral    |
      | Take-home     |
      | Final Round   |
      | Culture Fit   |
      | Other         |

  Scenario: Fail to create an interview when required fields are missing
    When I send a POST request to "/applications/{application_id}/interviews" with body:
      """
      {
        "time": "14:00",
        "type": "Technical"
      }
      """
    Then the response status code should be 422
    And the response body should contain a validation error for field "date"

  Scenario: Fail to create an interview with an invalid type
    When I send a POST request to "/applications/{application_id}/interviews" with body:
      """
      {
        "date": "2025-05-14",
        "time": "14:00",
        "type": "Lunch Chat"
      }
      """
    Then the response status code should be 422
    And the response body should contain a validation error for field "type"

  Scenario: Fail to create an interview with an invalid date format
    When I send a POST request to "/applications/{application_id}/interviews" with body:
      """
      {
        "date": "14-05-2025",
        "time": "14:00",
        "type": "Technical"
      }
      """
    Then the response status code should be 422
    And the response body should contain a validation error for field "date"

  Scenario: Fail to create an interview with an invalid time format
    When I send a POST request to "/applications/{application_id}/interviews" with body:
      """
      {
        "date": "2025-05-14",
        "time": "2pm",
        "type": "Technical"
      }
      """
    Then the response status code should be 422
    And the response body should contain a validation error for field "time"

  Scenario: Fail to create an interview for a non-existent application
    When I send a POST request to "/applications/99999/interviews" with body:
      """
      {
        "date": "2025-05-14",
        "time": "14:00",
        "type": "Technical"
      }
      """
    Then the response status code should be 404
    And the response body field "detail" should equal "Application not found"

  # ---------------------------------------------------------------------------
  # READ — single
  # ---------------------------------------------------------------------------

  Scenario: Successfully retrieve an existing interview by ID
    Given an interview exists for the application with:
      | field       | value         |
      | date        | 2025-05-14    |
      | time        | 14:00         |
      | type        | Technical     |
      | interviewer | Alex Park     |
    When I send a GET request to "/applications/{application_id}/interviews/{id}"
    Then the response status code should be 200
    And the response body field "type" should equal "Technical"
    And the response body field "interviewer" should equal "Alex Park"

  Scenario: Fail to retrieve an interview that does not exist
    When I send a GET request to "/applications/{application_id}/interviews/99999"
    Then the response status code should be 404
    And the response body field "detail" should equal "Interview not found"

  Scenario: Fail to retrieve an interview that belongs to a different application
    Given a second application exists
    And an interview exists for the second application with:
      | field | value     |
      | date  | 2025-06-01|
      | time  | 09:00     |
      | type  | Behavioral|
    When I send a GET request to "/applications/{application_id}/interviews/{second_interview_id}"
    Then the response status code should be 404

  # ---------------------------------------------------------------------------
  # READ — list
  # ---------------------------------------------------------------------------

  Scenario: Successfully retrieve all interviews for an application
    Given the following interviews exist for the application:
      | date       | time  | type          |
      | 2025-05-14 | 14:00 | Technical     |
      | 2025-05-18 | 10:00 | HR Interview  |
      | 2025-05-22 | 09:00 | Final Round   |
    When I send a GET request to "/applications/{application_id}/interviews"
    Then the response status code should be 200
    And the response body should be a list of 3 interviews

  Scenario: Retrieve an empty list when an application has no interviews
    When I send a GET request to "/applications/{application_id}/interviews"
    Then the response status code should be 200
    And the response body should be an empty list

  Scenario: Fail to list interviews for a non-existent application
    When I send a GET request to "/applications/99999/interviews"
    Then the response status code should be 404
    And the response body field "detail" should equal "Application not found"

  # ---------------------------------------------------------------------------
  # UPDATE
  # ---------------------------------------------------------------------------

  Scenario: Successfully update an interview's date and time
    Given an interview exists for the application with:
      | field | value      |
      | date  | 2025-05-14 |
      | time  | 14:00      |
      | type  | Technical  |
    When I send a PATCH request to "/applications/{application_id}/interviews/{id}" with body:
      """
      {
        "date": "2025-05-21",
        "time": "16:00"
      }
      """
    Then the response status code should be 200
    And the response body field "date" should equal "2025-05-21"
    And the response body field "time" should equal "16:00"

  Scenario: Successfully update an interview's notes and interviewer
    Given an interview exists for the application with:
      | field | value     |
      | date  | 2025-05-14|
      | time  | 14:00     |
      | type  | Technical |
    When I send a PATCH request to "/applications/{application_id}/interviews/{id}" with body:
      """
      {
        "notes": "Focus on distributed systems.",
        "interviewer": "Jane Smith"
      }
      """
    Then the response status code should be 200
    And the response body field "notes" should equal "Focus on distributed systems."
    And the response body field "interviewer" should equal "Jane Smith"

  Scenario: Successfully change an interview type
    Given an interview exists for the application with:
      | field | value        |
      | date  | 2025-05-14   |
      | time  | 14:00        |
      | type  | Phone Screen |
    When I send a PATCH request to "/applications/{application_id}/interviews/{id}" with body:
      """
      {
        "type": "System Design"
      }
      """
    Then the response status code should be 200
    And the response body field "type" should equal "System Design"

  Scenario: Fail to update an interview that does not exist
    When I send a PATCH request to "/applications/{application_id}/interviews/99999" with body:
      """
      {
        "notes": "Updated notes"
      }
      """
    Then the response status code should be 404
    And the response body field "detail" should equal "Interview not found"

  Scenario: Fail to update an interview with an invalid type
    Given an interview exists for the application with:
      | field | value     |
      | date  | 2025-05-14|
      | time  | 14:00     |
      | type  | Technical |
    When I send a PATCH request to "/applications/{application_id}/interviews/{id}" with body:
      """
      {
        "type": "Coffee Chat"
      }
      """
    Then the response status code should be 422
    And the response body should contain a validation error for field "type"

  # ---------------------------------------------------------------------------
  # DELETE
  # ---------------------------------------------------------------------------

  Scenario: Successfully delete an existing interview
    Given an interview exists for the application with:
      | field | value     |
      | date  | 2025-05-14|
      | time  | 14:00     |
      | type  | Technical |
    When I send a DELETE request to "/applications/{application_id}/interviews/{id}"
    Then the response status code should be 204
    And a subsequent GET request to "/applications/{application_id}/interviews/{id}" should return 404

  Scenario: Fail to delete an interview that does not exist
    When I send a DELETE request to "/applications/{application_id}/interviews/99999"
    Then the response status code should be 404
    And the response body field "detail" should equal "Interview not found"

  Scenario: Deleting an application also deletes its interviews
    Given an interview exists for the application with:
      | field | value     |
      | date  | 2025-05-14|
      | time  | 14:00     |
      | type  | Technical |
    When I send a DELETE request to "/applications/{application_id}"
    Then the response status code should be 204
    And a subsequent GET request to "/applications/{application_id}/interviews" should return 404

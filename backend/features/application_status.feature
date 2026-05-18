# features/application_status.feature

Feature: Application Status Transitions
  As a job seeker
  I want to transition an application's status through its lifecycle
  So that my tracker always reflects the real state of each application

  Background:
    Given the database is clean
    And the API is running

  # ---------------------------------------------------------------------------
  # Valid forward progressions
  # ---------------------------------------------------------------------------

  Scenario: Progress an application from Applied to Interviewing
    Given an application exists with status "Applied"
    When I send a PATCH request to "/applications/{id}" with body:
      """
      { "status": "Interviewing" }
      """
    Then the response status code should be 200
    And the response body field "status" should equal "Interviewing"

  Scenario: Progress an application from Interviewing to Offer
    Given an application exists with status "Interviewing"
    When I send a PATCH request to "/applications/{id}" with body:
      """
      { "status": "Offer" }
      """
    Then the response status code should be 200
    And the response body field "status" should equal "Offer"

  Scenario: Progress an application from Offer to Accepted
    Given an application exists with status "Offer"
    When I send a PATCH request to "/applications/{id}" with body:
      """
      { "status": "Accepted" }
      """
    Then the response status code should be 200
    And the response body field "status" should equal "Accepted"

  # ---------------------------------------------------------------------------
  # Valid terminal / side transitions
  # ---------------------------------------------------------------------------

  Scenario Outline: Mark an application as Rejected from any active status
    Given an application exists with status "<from_status>"
    When I send a PATCH request to "/applications/{id}" with body:
      """
      { "status": "Rejected" }
      """
    Then the response status code should be 200
    And the response body field "status" should equal "Rejected"

    Examples:
      | from_status  |
      | Applied      |
      | Interviewing |
      | Offer        |

  Scenario Outline: Mark an application as Ghosted from any active status
    Given an application exists with status "<from_status>"
    When I send a PATCH request to "/applications/{id}" with body:
      """
      { "status": "Ghosted" }
      """
    Then the response status code should be 200
    And the response body field "status" should equal "Ghosted"

    Examples:
      | from_status  |
      | Applied      |
      | Interviewing |
      | Offer        |

  # ---------------------------------------------------------------------------
  # Dashboard / summary stats
  # ---------------------------------------------------------------------------

  Scenario: Retrieve a summary of applications grouped by status
    Given the following applications exist:
      | position           | company | status       |
      | Frontend Developer | Acme    | Applied      |
      | Backend Engineer   | Beta    | Applied      |
      | Data Scientist     | Gamma   | Interviewing |
      | DevOps Engineer    | Delta   | Offer        |
      | QA Engineer        | Epsilon | Rejected     |
      | ML Engineer        | Zeta    | Ghosted      |
    When I send a GET request to "/applications/summary"
    Then the response status code should be 200
    And the response body should contain:
      | status       | count |
      | Applied      | 2     |
      | Interviewing | 1     |
      | Offer        | 1     |
      | Accepted     | 0     |
      | Rejected     | 1     |
      | Ghosted      | 1     |

  Scenario: Summary returns zero counts for all statuses when no applications exist
    When I send a GET request to "/applications/summary"
    Then the response status code should be 200
    And every status in the summary should have count 0

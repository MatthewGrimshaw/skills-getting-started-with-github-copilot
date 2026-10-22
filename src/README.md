# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- See signed-up participants on each activity card, updated after signup or removal
- Sign up for activities
- Unregister participants using the delete icon next to their email address

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a participant from an activity                          |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

## Backend Tests

From the repository root, install dependencies and run the tests:

```bash
python -m pip install -r requirements.txt
python -m pytest tests -q
```

To run a single test module:

```bash
python -m pytest tests/test_signup.py -q
```

The [tests directory](../tests/) uses pytest and FastAPI's TestClient, so no
running server is required. Shared fixtures provide deterministic activity data
for each test and restore the original in-memory data afterward, even if a test
fails.

Every test follows the Arrange-Act-Assert (AAA) pattern:

1. **Arrange:** Prepare activity data and request inputs.
2. **Act:** Make the API request being tested.
3. **Assert:** Check the status code, response body, and resulting activity state.

Coverage includes activity listing, signup and unregister success and error
cases, capacity boundaries, re-registration, and homepage redirects and serving.
Rejected requests are checked to ensure they do not change activity data.
Browser rendering and automatic card refresh are outside this backend suite.

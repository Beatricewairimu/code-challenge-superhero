# Heroes API

This is a Flask API for tracking heroes and their superpowers.

## Setup

1. Clone the repository.
2. Install the required packages:
   ```
   pip install Flask Flask-SQLAlchemy
   ```
3. Run the application:
   ```
   python app.py
   ```

## Endpoints

- `GET /episodes`: Returns a list of episodes.
- `GET /episodes/:id`: Returns details of a specific episode.
- `GET /guests`: Returns a list of guests.
- `POST /appearances`: Creates a new appearance.

## Database

The API uses SQLite for the database. The database file is `heroes.db`.

## Postman Collection

Import the provided Postman collection to test the API endpoints.

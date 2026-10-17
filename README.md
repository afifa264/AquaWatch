# AquaWatch — Water Quality and Leakage Reporting System

A polished, responsive Flask web application for a community to report water leakage, water-quality concerns, low pressure, and water logging. It includes a premium teal/sea-glass UI, searchable report board, priority/status labels, a small dashboard, user registration/login, and SQLite storage.

## Tech stack
- Python 3.10+
- Flask
- SQLite
- HTML, CSS, JavaScript

## Run locally
1. Extract `AquaWatch.zip`.
2. Open the `aquawatch_project` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000`.

The SQLite database (`aquawatch.db`) is created automatically on first run and receives a few demo reports. Register an account to submit reports. In this demo, a user can mark only their own report as resolved.

## Main pages
- `/` — Home and dashboard overview
- `/reports` — Search and filter community reports
- `/report/new` — Submit a report (sign-in required)
- `/reports/<id>` — Report details and status
- `/register` and `/login` — Account access
- `/about` — Project purpose and limitations

## Important project notes
- Reports are community observations, not verified water tests.
- The app is an academic demo; it does not automatically contact water authorities or provide emergency response.
- Before public deployment, set a strong `SECRET_KEY` environment variable, turn off Flask debug mode, add CSRF protection and rate limiting, and review security/privacy practices.
- The demo uses seeded reports for presentation; remove the generated `aquawatch.db` if you want a clean database (stop the app first).

## Suggested AAT-1 demo flow
1. Show the landing page and live report statistics.
2. Open **Reports** and demonstrate search/category/status filters.
3. Register a test account and sign in.
4. Submit a sample leakage or water-quality concern.
5. Open the report detail page and mark your own report as resolved.
6. Explain that the dashboard updates from SQLite records.

AquaWatch – Water Quality and Leakage Reporting System
About the Project

AquaWatch is a web-based water conservation and management system developed to help communities report water-related problems, including water leakage and water quality concerns. It provides a centralized platform to submit reports, view reported issues, and track their resolution status.

The main goal of AquaWatch is to encourage community participation, promote water conservation, and improve awareness of local water-related problems.

Objectives
Provide an easy-to-use platform for reporting water leakage.
Allow users to report water quality concerns.
Help users search and filter reported issues.
Track the status and priority of reports.
Display dashboard statistics for better monitoring.
Promote responsible water usage and community awareness.
Features
User Authentication: User registration and login.
Report Submission: Submit water-related issues with descriptions and locations.
Report Management: View, search, and filter reports.
Status Tracking: Track report progress and mark eligible reports as resolved.
Dashboard: Display statistics about reports and their statuses.
Responsive Interface: A modern interface designed for convenient use.
Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: Python, Flask
Database: SQLite
Development Environment: Visual Studio Code
Version Control: Git and GitHub
Project Structure
AquaWatch/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
└── static/

Installation and Setup
1. Clone the Repository
git clone YOUR_GITHUB_REPOSITORY_URL

2. Open the Project Folder
cd AquaWatch

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
python app.py

5. Open in a Browser

Visit:

http://127.0.0.1:5000

How It Works
A user registers and logs in to the application.
The user submits a water leakage or water quality concern.
The application stores the report in the SQLite database.
Users can view, search, and filter submitted reports.
Report status and dashboard statistics reflect the stored records.
Future Enhancements
Integration with maps to visualize report locations.
Notifications when report statuses change.
Integration with verified water quality sensor data.
Administrative tools for managing and reviewing reports.
Deployment to a cloud hosting platform.
Limitations

Water quality reports are community observations and are not laboratory-verified water tests. The application does not automatically contact water authorities.

Conclusion

AquaWatch provides a digital platform for community-based water issue reporting and tracking. It aims to support water conservation, improve awareness, and encourage communities to take an active role in identifying water-related problems.

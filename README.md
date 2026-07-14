Hospital Management System

A full-stack web application built with Django to digitize appointment scheduling, staff leave management, patient records, and hospital-wide announcements — with a clean, role-based UI for non-technical staff.

Tech Stack


Backend: Python, Django
Database: MySQL
Frontend: HTML, CSS
Config/Secrets: python-decouple


Features


Role-based access control — three user roles (Admin, Doctor, Staff) via a custom AbstractUser model, enforced through centralized role_required / roles_required decorators
Patient records — managed as data records by staff/admin (patients are not system users)
Appointment booking — 2-day advance booking window, morning/afternoon/night slots, configurable max bookings per slot per doctor
Leave management — staff leave requests with an approval workflow and status tracking
Announcements — broadcast system for hospital-wide notices
Security — login rate limiting via Django's cache framework, CSRF protection, environment-based credential management, IDOR-safe view access checks


App Structure

The project is organized into five independent Django apps:

AppResponsibilityaccountsAuthentication, custom user model, rolespatientsPatient record managementappointmentsScheduling, booking, cancellationleavesStaff leave requests and approvalsannouncementsBroadcast messaging

Design System


Layout: Dark navy sidebar, white content area on a soft canvas background
Typography: Fraunces (display headings), Inter (UI text), JetBrains Mono (stat numbers)
Accent color: Clinical blue (#155EEF)
Signature element: Animated ECG/heartbeat SVG
CSS architecture: Unified class naming system (ph, stats, tbl-wrap, card, badge, btn, etc.) so style changes cascade globally instead of being edited per template


Local Setup


Clone the repository


bash   git clone https://github.com/nsyamsuresh/<repo-name>.git
   cd <repo-name>


Create and activate a virtual environment


bash   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate


Install dependencies


bash   pip install -r requirements.txt


Create a .env file in the project root (never commit this file) with:


   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=your-db-name
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_HOST=localhost
   DB_PORT=3306


Set up the MySQL database, then run migrations


bash   python manage.py migrate


Create a superuser


bash   python manage.py createsuperuser


Run the development server


bash   python manage.py runserver


Visit http://127.0.0.1:8000/ in your browser



Note: This project runs locally and is not currently deployed to a hosting platform.



Security Notes


DEBUG should be set to False outside local development
All credentials are loaded from environment variables, never hardcoded
CSRF protection is enabled on all forms
Role-based permission checks are enforced server-side on every view — not just hidden via UI


Author

Syam Suresh
github.com/nsyamsuresh

Contributor
Sneha S
github.com/ssnehaasuresh

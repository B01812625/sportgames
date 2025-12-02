Paisley Highland Games Event Registration System – Development Document**

Document Information**
Project Name: Paisley Highland Games Event Registration System
Document Version: v1.0
Development Year: 2025
Core Functions: Event management, user registration and login, application submission and review
Intended Users: Developers, maintenance personnel, project managers

1. Project Overview**

1.1 Project Introduction
Paisley Highland Games is a lightweight event registration and management system designed for schools and event organizers. It supports user registration and login, event browsing, online application submission, file upload, and full-process management of events and applications by administrators. It features a responsive design that adapts to both PC and mobile devices.

1.2 Core Objectives
• Simplify the event registration process and reduce participation barriers
• Provide efficient tools for application review and event management
• Ensure user data security and meet basic GDPR compliance requirements
• Offer a clear and user-friendly interaction experience for both front-end and back-end

2. Technology Stack Description**

2.1 Backend Technologies
Python 3.8+: Main backend development language
Flask 2.x: Lightweight web framework for routing and template rendering
Flask-SQLAlchemy 3.x: ORM framework for simplified model definition and database queries
Flask-Login 0.6.x: User authentication and session management
Flask-WTF 1.2.x: Form validation and CSRF protection
Flask-Bcrypt 1.0.x: Secure password hashing
SQLite 3.x: Lightweight relational database for development/testing

2.2 Frontend Technologies
HTML5/CSS3: Page structure and core styles
JavaScript ES6+: Front-end logic (validation, animations)
Bootstrap 5.3.x: Responsive UI framework
Bootstrap Icons 1.10.x: Icon library
Jinja2: Template engine for dynamic rendering

2.3 Development / Tool Support
PyCharm / VS Code: Code editing
Git: Version control
pip: Dependency installation
Flask-Migrate (optional): Database migration tool

3. Project Structure**

sportgames/ – Project root directory
.venv/ – Python virtual environment
app/ – Core application directory
app/**init**.py – Application initialization
app/models/ – Data model layer
user.py – User model (authentication, permissions)
competition.py – Competition model
application.py – Application model
app/routes/ – Route handlers
auth.py – Registration, login, logout, profile
admin.py – Admin dashboard, event/application management
competitions.py – Event list, details, application submission
app/forms/ – Form definitions and validation
auth_forms.py – Registration/Login
competition_forms.py – Event creation/edit
application_forms.py – Application submission/review
app/templates/ – HTML templates
base.html – Base layout
auth/ – Registration/login pages
admin/ – Admin management pages
competitions/ – Event pages
app/static/ – CSS, JS, images, documents
instance/site.db – SQLite database file
create_db.py – Database initialization (default admin + test events)
run.py – Application startup entry
requirements.txt – Dependency list
README.md – Project manual

3.1 Core Directory Responsibilities
app/models/: Defines data models and relationships
app/routes/: URL routing and view functions
app/forms/: Form fields and validation rules
app/templates/: HTML templates rendered by Jinja2
app/static/: Static resources (CSS/JS/images/docs)
instance/site.db: Database storing all business data
create_db.py: Initializes tables and default data
run.py: Starts Flask development server

4. Core Function Modules**

4.1 User Authentication
User Registration: Collect username, email, password, GDPR consent; hash password
User Login: Validate credentials and maintain session
User Logout: Clear session and redirect
User Profile: View/edit personal info and delete account
Account Deletion: Cascade delete related applications and files

4.2 Event Management
Event List: Paginated display with name, category, date, status
Event Details: Full event info (rules, time, deadlines)
Event Creation (Admin): Create new event entry
Event Editing (Admin): Edit existing event
Registration Status Check: Auto-determine whether the event is still open

4.3 Application Management
Online Application Submission: Users submit information and upload documents
Application List: Users view their own applications
Application Review (Admin): Approve/reject with remarks
File Download (Admin): Download user-uploaded files

4.4 Administrator Core Functions
Admin Dashboard: Display statistics (user count, event count, pending applications)
Event Management List: Create/edit/delete events
Application Review List: Filter applications by status
Application Review Page: Full details + update approval status

5. Environment Setup and Startup Steps**

5.1 Development Environment Setup
Requirements: Python 3.8+, Git (optional)

Step 1: Clone the project
git clone <repository>
cd sportgames

Step 2: Create and activate virtual environment
Windows: python -m venv .venv / .venv\Scripts\activate
Mac/Linux: python3 -m venv .venv / source .venv/bin/activate

Step 3: Install dependencies
pip install -r requirements.txt

Step 4: Initialize the database
python create_db.py
This generates site.db, creates default admin (admin / Admin123! / [admin@phg.com](mailto:admin@phg.com)), and adds 3 test events.

Step 5: Start the development server
python run.py
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

5.2 Dependency List
Flask==2.3.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
Flask-Bcrypt==1.0.1
Werkzeug==2.3.7
Jinja2==3.1.2
python-dotenv==1.0.0

6. Deployment Instructions**

6.1 Development Environment
Use Flask built-in server
Start: python run.py
URL: [http://127.0.0.1:5000](http://127.0.0.1:5000)

6.2 Production Environment
Install Gunicorn: pip install gunicorn
Start server:
gunicorn -w 4 -b 0.0.0.0:8000 "run:app"

(Optional) Configure Nginx:
Forward port 80 → 127.0.0.1:8000
Enable static file caching

7. Data Model Relationships**

7.1 Core Model Relationships
User – Application: One-to-many (user submits many applications; cascade deletion)
Competition – Application: One-to-many (event receives many applications)
Application – User: Many-to-one
Application – Competition: Many-to-one

7.2 Key Model Fields
User: id, username, email, password_hash, is_admin, consent_given
Competition: id, name, category, start_date, application_deadline, description
Application: id, user_id, competition_id, team_name, document_filename, status, submission_date

8. Compliance (GDPR)**
• GDPR consent checkbox stored in consent_given
• Cascade deletion supports “right to be forgotten”
• Privacy policy accessible in footer


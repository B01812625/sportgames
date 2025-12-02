"""
Database Initialization Script: Create all tables + Add admin account + Sample competitions
Execution command: python create_db.py
"""
import os
import sys
from datetime import datetime, timedelta

# Add project root directory to Python path (ensure app can be imported)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core modules
from app import create_app, db
from app.models.user import User
from app.models.competition import Competition
from app.models.application import Application
from flask_bcrypt import generate_password_hash

def create_database():
    """Main function for database initialization"""
    print("=" * 50)
    print("📦 Starting database initialization...")
    print("=" * 50)

    # 1. Create Flask app instance and activate context
    app = create_app()
    with app.app_context():
        try:
            # 2. Check if database file already exists
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            if os.path.exists(db_path):
                print(f"⚠️ Existing database file found: {db_path}")
                choice = input("Overwrite existing database? (y/n, default n): ").strip().lower()
                if choice != 'y':
                    print("❌ Initialization cancelled, retaining existing database")
                    return
                # Delete old database file
                os.remove(db_path)
                print("✅ Old database file deleted successfully")

            # 3. Create all tables corresponding to models
            db.create_all()
            print("✅ All database tables created successfully!")

            # 4. Add admin account (unique)
            admin_username = "admin"
            admin_email = "admin@phg.com"
            admin_password = "Admin123!"  # Default password, can be modified later

            if not User.query.filter_by(username=admin_username).first():
                admin = User(
                    username=admin_username,
                    email=admin_email,
                    password_hash=generate_password_hash(admin_password).decode("utf-8"),
                    is_admin=True,
                    consent_given=True,
                    created_at=datetime.utcnow()
                )
                db.session.add(admin)
                db.session.commit()
                print("\n✅ Admin account created successfully:")
                print(f"   Username: {admin_username}")
                print(f"   Password: {admin_password}")
                print(f"   Email: {admin_email}")
            else:
                print("\n⚠️ Admin account already exists, skipping creation")

            # 5. Add sample competitions (3 items)
            if Competition.query.count() == 0:
                sample_competitions = [
                    Competition(
                        name="2025 Highland Dance Competition",
                        category="Individual",
                        start_date=datetime.utcnow() + timedelta(days=30),
                        application_deadline=datetime.utcnow() + timedelta(days=15),
                        description="Traditional Scottish Highland dance competition, divided into solo jazz dance and duet tap dance categories. Contestants must submit a dance video as application material. Judges will score based on movement standardization and sense of rhythm."
                    ),
                    Competition(
                        name="Bagpipe Ensemble Competition",
                        category="Team",
                        start_date=datetime.utcnow() + timedelta(days=45),
                        application_deadline=datetime.utcnow() + timedelta(days=20),
                        description="Team bagpipe performance competition. Each team consists of 3-5 members. Contestants must perform the designated traditional Scottish tune 'Scotland the Brave' with a performance duration of 5 minutes. Scoring criteria include tone, coordination, and expressiveness."
                    ),
                    Competition(
                        name="Highland Weightlifting Challenge",
                        category="Mixed",
                        start_date=datetime.utcnow() + timedelta(days=60),
                        application_deadline=datetime.utcnow() + timedelta(days=30),
                        description="Traditional Highland strength competition, divided into individual and team relay categories. The weight for the individual category is 50kg, and the total relay weight for the team category (3 members) is 120kg. Rankings are determined by completion time."
                    )
                ]
                db.session.add_all(sample_competitions)
                db.session.commit()
                print("\n✅ 3 sample competitions added successfully:")
                for i, comp in enumerate(sample_competitions, 1):
                    print(f"   {i}. {comp.name} ({comp.category})")
                    print(f"      Event Date: {comp.start_date.strftime('%Y-%m-%d')}")
            else:
                print("\n⚠️ Competition data already exists, skipping sample competition addition")

            # 6. Commit all changes
            db.session.commit()
            print("\n" + "=" * 50)
            print("🎉 Database initialization completed successfully!")
            print(f"📁 Database file path: {db_path}")
            print("💡 Next step: Run 'python run.py' to start the project")
            print("=" * 50)

        except Exception as e:
            # Rollback transaction on error
            db.session.rollback()
            print(f"\n❌ Database initialization failed: {str(e)}")
            print("💡 Please check:")
            print("   1. Are all project dependencies installed? (pip install -r requirements.txt)")
            print("   2. Do model files exist and have no syntax errors?")
            print("   3. Does the project directory have read/write permissions?")
            sys.exit(1)

if __name__ == "__main__":
    create_database()
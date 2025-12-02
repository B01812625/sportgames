from app import create_app, db
from app.models.user import User
from app.models.competition import Competition

app = create_app()

# Command line: Initialize database and add test data
@app.cli.command("init-db")
def init_db():
    """Initialize database and add test data (admin account + sample competitions)"""
    db.create_all()
    print("Database created successfully!")

    # Add admin account (Username: admin, Password: Admin123!, Email: admin@phg.com)
    if not User.query.filter_by(is_admin=True).first():
        admin = User(
            username='admin',
            email='admin@phg.com',
            password='Admin123!',  # Automatically encrypted
            consent_given=True,
            is_admin=True
        )
        db.session.add(admin)
        print("Admin account created successfully:")
        print("Username: admin | Password: Admin123! | Email: admin@phg.com")

    # Add sample competitions
    if not Competition.query.first():
        competitions = [
            Competition(
                name='Highland Dance Competition',
                description='Traditional Scottish Highland dance competition, divided into solo and duet categories. Performances must follow traditional dance steps.',
                category='Individual/Team',
                start_date='2025-08-15 10:00:00',
                application_deadline='2025-07-30 23:59:59'
            ),
            Competition(
                name='Scottish Bagpipe Performance',
                description='Bagpipe solo or ensemble competition. Repertoire must include traditional Scottish folk songs.',
                category='Individual/Team',
                start_date='2025-08-16 09:30:00',
                application_deadline='2025-08-05 23:59:59'
            ),
            Competition(
                name='Highland Weightlifting Challenge',
                description='Traditional Highland strength competition, including stone ball throwing, wooden pole lifting and other events.',
                category='Individual',
                start_date='2025-08-17 14:00:00',
                application_deadline='2025-08-10 23:59:59'
            )
        ]
        db.session.add_all(competitions)
        print("3 sample competitions added successfully!")

    db.session.commit()
    print("Initialization completed!")

if __name__ == '__main__':
    app.run(debug=True)
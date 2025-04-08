"""
Script to test database queries and check existing applications
"""
from datetime import datetime
from app import app, db
from models import Application

def check_applications():
    """Check applications in the database"""
    with app.app_context():
        # Count all applications
        count = Application.query.count()
        print(f"Total applications in database: {count}")
        
        # Check for specific application
        application = Application.query.filter_by(nric="721231-10-6065").first()
        if application:
            print(f"Found application for {application.full_name}")
            print(f"NRIC: {application.nric}")
            print(f"Assistance Type: {application.assistance_type}")
            print(f"Status: {application.status}")
            print(f"Application Date: {application.application_date}")
            print(f"Approval Date: {application.approval_date}")
            print(f"Grace Period End: {application.grace_period_end}")
            if application.grace_period_end:
                print(f"Days remaining in grace period: {(application.grace_period_end - datetime.now()).days}")
            else:
                print("No grace period set")
        else:
            print("No application found for NRIC 721231-10-6065")

if __name__ == "__main__":
    check_applications()
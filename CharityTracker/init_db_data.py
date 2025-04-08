"""
Script to initialize database with previous application data
"""
from datetime import datetime, timedelta
from app import app, db
from models import Application

def add_previous_applications():
    """Add previous applications to database"""
    with app.app_context():
        # Check if MOHD ZAID's application already exists
        existing = Application.query.filter_by(nric="721231-10-6065").first()
        
        # Create or update application for MOHD ZAID from March 18, 2025
        application_date = datetime(2025, 3, 18)
        approval_date = application_date
        
        if existing:
            print(f"Application for MOHD ZAID already exists with status: {existing.status}")
            print(f"Updating application dates...")
            
            # Update the existing record
            existing.application_date = application_date
            existing.approval_date = approval_date
            
            if existing.assistance_type == "Baucer":
                existing.grace_period_end = approval_date + timedelta(days=90)  # 3 months
            elif existing.assistance_type == "TRM":
                existing.grace_period_end = approval_date + timedelta(days=180)  # 6 months
                
            db.session.commit()
            print(f"Updated application for {existing.full_name}")
            print(f"New application date: {existing.application_date}")
            print(f"New approval date: {existing.approval_date}")
            print(f"New grace period ends: {existing.grace_period_end}")
            print(f"Days remaining in grace period: {(existing.grace_period_end - datetime.now()).days}")
            return
        
        # If no existing record, create a new one
        mohd_zaid = Application(
            full_name="MOHD ZAID BIN ZAINAL ABIDIN",
            nric="721231-10-6065",
            phone="0123456789",
            assistance_type="Baucer",  # Adjust if it was TRM
            application_date=application_date,
            status="Approved"
        )
        
        # Manually set the approval date and calculate grace period
        mohd_zaid.approval_date = approval_date
        if mohd_zaid.assistance_type == "Baucer":
            mohd_zaid.grace_period_end = approval_date + timedelta(days=90)  # 3 months
        elif mohd_zaid.assistance_type == "TRM":
            mohd_zaid.grace_period_end = approval_date + timedelta(days=180)  # 6 months
            
        db.session.add(mohd_zaid)
        db.session.commit()
        print(f"Added application for {mohd_zaid.full_name}")
        print(f"Approval date: {mohd_zaid.approval_date}")
        print(f"Grace period ends: {mohd_zaid.grace_period_end}")
        print(f"Days remaining in grace period: {(mohd_zaid.grace_period_end - datetime.now()).days}")

if __name__ == "__main__":
    add_previous_applications()
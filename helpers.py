from datetime import datetime
from models import Application
from app import db

def format_date(date_obj):
    """Format date object to string"""
    if not date_obj:
        return "N/A"
    return date_obj.strftime("%d %b %Y")

def get_all_applications():
    """Retrieve all applications from the database"""
    return Application.query.order_by(Application.application_date.desc()).all()

def get_application_by_id(app_id):
    """Retrieve an application by its ID"""
    return Application.query.get(app_id)

def create_application(form_data):
    """Create a new application from form data"""
    application = Application(
        full_name=form_data.full_name.data,
        nric=form_data.nric.data,
        phone=form_data.phone.data,
        assistance_type=form_data.assistance_type.data,
        application_date=form_data.application_date.data
    )
    
    db.session.add(application)
    db.session.commit()
    return application

def update_application_status(app_id, status):
    """Update the status of an application"""
    application = get_application_by_id(app_id)
    
    if not application:
        return None
    
    if status == "Approved":
        application.approve()
    elif status == "Rejected":
        application.reject()
    else:
        application.status = status
    
    db.session.commit()
    return application

def filter_applications(status=None, assistance_type=None, search_term=None):
    """Filter applications based on provided criteria"""
    query = Application.query
    
    if status:
        query = query.filter(Application.status == status)
    
    if assistance_type:
        query = query.filter(Application.assistance_type == assistance_type)
    
    if search_term:
        search = f"%{search_term}%"
        query = query.filter(
            (Application.full_name.ilike(search)) |
            (Application.nric.ilike(search)) |
            (Application.phone.ilike(search))
        )
    
    return query.order_by(Application.application_date.desc()).all()

def check_grace_period(nric, assistance_type):
    """
    Check if applicant has an existing approved application within grace period
    Returns True if within grace period, False otherwise
    """
    now = datetime.now()
    
    # Find the most recent approved application for this user and assistance type
    previous_application = Application.query.filter(
        Application.nric == nric,
        Application.assistance_type == assistance_type,
        Application.status == "Approved",
        Application.grace_period_end >= now  # Still within grace period
    ).order_by(Application.approval_date.desc()).first()
    
    # If a previous application exists and is still in grace period, return True
    return previous_application is not None

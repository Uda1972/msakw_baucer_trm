from datetime import datetime, timedelta
from app import db

class Application(db.Model):
    """Model for assistance applications"""
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    nric = db.Column(db.String(14), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    assistance_type = db.Column(db.String(20), nullable=False)  # 'Baucer' or 'TRM'
    application_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='Processing')  # 'Approved', 'Rejected', 'Processing'
    approval_date = db.Column(db.DateTime, nullable=True)
    grace_period_end = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, full_name, nric, phone, assistance_type, application_date=None, status="Processing"):
        self.full_name = full_name
        self.nric = nric
        self.phone = phone
        self.assistance_type = assistance_type
        
        if application_date:
            self.application_date = application_date
        else:
            self.application_date = datetime.utcnow()
            
        self.status = status
        
        # If the application is created as already approved, calculate grace period
        if status == "Approved":
            self.approve()
    
    def approve(self):
        """Mark application as approved and calculate grace period end date"""
        self.status = "Approved"
        self.approval_date = datetime.utcnow()
        
        # Calculate grace period based on assistance type
        if self.assistance_type == "Baucer":
            self.grace_period_end = self.approval_date + timedelta(days=90)  # 3 months
        elif self.assistance_type == "TRM":
            self.grace_period_end = self.approval_date + timedelta(days=180)  # 6 months
        
        return self
    
    def reject(self):
        """Mark application as rejected"""
        self.status = "Rejected"
        self.approval_date = datetime.utcnow()
        self.grace_period_end = None
        
        return self
    
    def to_dict(self):
        """Convert application to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'nric': self.nric,
            'phone': self.phone,
            'assistance_type': self.assistance_type,
            'application_date': self.application_date.strftime('%Y-%m-%d'),
            'status': self.status,
            'approval_date': self.approval_date.strftime('%Y-%m-%d') if self.approval_date else None,
            'grace_period_end': self.grace_period_end.strftime('%Y-%m-%d') if self.grace_period_end else None
        }

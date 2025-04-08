from flask import render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime, timedelta
from collections import deque
import time

from app import app
from forms import ApplicationForm

def check_rate_limit():
    """Allow 20 submissions within 1 hour"""
    now = time.time()
    if 'submission_times' not in session:
        session['submission_times'] = []
        session.permanent = True  # Make session persist longer
    
    # Convert stored string times back to float
    times = deque([float(t) for t in session['submission_times']], maxlen=20)
    
    # Remove submissions older than 1 hour
    while times and now - times[0] > 3600:  # 3600 seconds = 1 hour
        times.popleft()
    
    # Check if we've hit the limit
    if len(times) >= 20:
        return False
        
    times.append(now)
    session['submission_times'] = list(times)  # Convert back to list for session storage
    return True
from helpers import (
    get_all_applications, get_application_by_id, 
    create_application, update_application_status,
    filter_applications, format_date, check_grace_period
)

@app.route('/')
def index():
    """Home page with application form and recent applications"""
    form = ApplicationForm()
    # Default to today's date
    form.application_date.data = datetime.now().date()
    
    # Get the five most recent applications
    recent_applications = get_all_applications()[:5]
    
    return render_template(
        'index.html', 
        form=form, 
        applications=recent_applications,
        format_date=format_date
    )

@app.route('/application', methods=['POST'])
def submit_application():
    """Handle application form submission"""
    if not check_rate_limit():
        flash('Please wait a few minutes before submitting again.', 'warning')
        return redirect(url_for('index'))
        
    form = ApplicationForm()
    
    if form.validate_on_submit():
        application = create_application(form)
        flash('Permohonan berjaya dihantar!', 'success')
        
        # Check if applicant is still within grace period
        in_grace_period = check_grace_period(form.nric.data, form.assistance_type.data)
        
        if in_grace_period:
            # Automatically reject if still in grace period
            status = "Rejected"
            flash(f'Permohonan ditolak kerana masih dalam tempoh penangguhan.', 'warning')
        else:
            # Auto-approve if not in grace period (for demonstration purposes)
            # In a real application, this would be handled by an admin approval process
            status = "Approved" if form.assistance_type.data in ["Baucer", "TRM"] else "Processing"
        
        update_application_status(application.id, status)
        
        return redirect(url_for('view_applications'))
    
    # If form validation fails, show errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", "danger")
    
    return redirect(url_for('index'))

@app.route('/applications')
def view_applications():
    """View all applications with filtering options"""
    status = request.args.get('status', '')
    assistance_type = request.args.get('type', '')
    search = request.args.get('search', '')
    
    if status or assistance_type or search:
        applications = filter_applications(status, assistance_type, search)
    else:
        applications = get_all_applications()
    
    return render_template(
        'applications.html',
        applications=applications,
        current_status=status,
        current_type=assistance_type,
        current_search=search,
        format_date=format_date
    )

@app.route('/application/<int:app_id>')
def view_application(app_id):
    """View a single application details"""
    application = get_application_by_id(app_id)
    
    if not application:
        flash('Permohonan tidak dijumpai', 'danger')
        return redirect(url_for('view_applications'))
    
    return render_template(
        'application_form.html', 
        application=application,
        format_date=format_date
    )

@app.route('/application/<int:app_id>/status', methods=['POST'])
def change_status(app_id):
    """Change the status of an application"""
    status = request.form.get('status')
    
    if not status or status not in ['Approved', 'Rejected', 'Processing']:
        flash('Status tidak sah', 'danger')
        return redirect(url_for('view_application', app_id=app_id))
    
    # Get application details
    application = get_application_by_id(app_id)
    if not application:
        flash('Permohonan tidak dijumpai', 'danger')
        return redirect(url_for('view_applications'))
    
    # Only check grace period if trying to approve
    if status == "Approved":
        # Check if applicant is still within grace period
        in_grace_period = check_grace_period(application.nric, application.assistance_type)
        
        if in_grace_period:
            flash('Permohonan tidak boleh diluluskan kerana masih dalam tempoh penangguhan.', 'warning')
            return redirect(url_for('view_application', app_id=app_id))
    
    # Process status change
    application = update_application_status(app_id, status)
    
    if not application:
        flash('Permohonan tidak dijumpai', 'danger')
    else:
        flash(f'Status permohonan dikemaskini kepada {status}', 'success')
    
    return redirect(url_for('view_application', app_id=app_id))

@app.context_processor
def utility_processor():
    """Make helper functions available in templates"""
    return {
        'format_date': format_date,
        'now': datetime.now
    }

@app.template_filter('format_date')
def format_date_filter(date):
    """Template filter to format dates"""
    return format_date(date)

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from datetime import datetime

class ApplicationForm(FlaskForm):
    """Form for creating a new assistance application"""
    full_name = StringField('Nama Penuh (Full Name)', 
                           validators=[DataRequired(), Length(min=3, max=100)])
    
    nric = StringField('No Kad Pengenalan (NRIC No)', 
                      validators=[
                          DataRequired(), 
                          Regexp(r'^\d{6}-\d{2}-\d{4}$', 
                                message='NRIC must be in format: XXXXXX-XX-XXXX')
                      ])
    
    phone = StringField('No Telefon (Telephone No)', 
                       validators=[
                           DataRequired(), 
                           Regexp(r'^(\+?6?01)[0-46-9]-*[0-9]{7,8}$', 
                                 message='Please enter a valid Malaysian phone number (e.g., 0123456789 or +60123456789)')
                       ])
    
    assistance_type = SelectField('Jenis Bantuan (Type of Assistance)', 
                                 choices=[
                                     ('Baucer', 'Baucer (3 months grace period)'), 
                                     ('TRM', 'Tabung Rahmah Madani (TRM) (6 months grace period)')
                                 ],
                                 validators=[DataRequired()])
    
    application_date = DateField('Tarikh Permohonan (Application Date)', 
                                format='%Y-%m-%d',
                                validators=[DataRequired()])
    
    submit = SubmitField('Submit Application')
    
    def validate_application_date(self, field):
        """Validation removed to allow testing with future dates"""
        # Future date validation temporarily disabled for testing
        pass

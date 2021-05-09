from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError, Regexp
from app import Contact

class newContactForm(FlaskForm):
    only_letters_regex = r"^[a-zA-Z\u00C0-\u017F\s]+$"
    PhoneNumber_regex = r"^[+]*[\d]{0,4}[\d]{3,4}[0-9]{7,9}$"
    email_regex = r'^[-\w.]+@([-\w]+\.)+[-\w]{2,4}$'

    FirstName = StringField('First Name',
                           validators=[DataRequired(),  Length(min=2, max=20), Regexp(only_letters_regex, message="This field must contain alphabetic characters only")])
    LastName = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20), Regexp(only_letters_regex, message="This field must contain alphabetic characters only")])
    Company = StringField('Company',
                           validators=[Optional(), Length(min=2, max=20)])   
    PhoneNumber = StringField('Phone Number',
                           validators=[Optional(), Length(min=2, max=20), Regexp(PhoneNumber_regex, message="This field must contain a valid phone number input (10 digits)")])                        
    Email = StringField('Email',
                        validators=[DataRequired(), Email(), Regexp(email_regex, message="This field must a valid email adress")])
    submit = SubmitField('Submit contact')

    def validate_PhoneNumber(self, PhoneNumber):
        contact = Contact.query.filter_by(PhoneNumber=PhoneNumber.data).first()
        if contact:
            raise ValidationError('That phone number is taken. Please choose a different one.')

    def validate_Email(self, Email):
        contact = Contact.query.filter_by(Email=Email.data).first()
        if contact:
            raise ValidationError('That email is taken. Please choose a different one.')
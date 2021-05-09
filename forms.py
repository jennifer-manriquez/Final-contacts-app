from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError

class newContactForm(FlaskForm):
    FirstName = StringField('First Name',
                           validators=[DataRequired(),  Length(min=2, max=20)])
    LastName = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Company = StringField('Company',
                           validators=[Optional(), Length(min=2, max=20)])   
    PhoneNumber = StringField('Phone Number',
                           validators=[Optional(), Length(min=2, max=20)])                        
    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Submit contact')

    #def validate_PhoneNumber(self, phone_number):
    #    contact = Contact.query.filter_by(PhoneNumber=phone_number.data).first()
    #    if contact:
    #        raise ValidationError('That phone number is taken. Please choose a different one.')

    #def validate_Email(self, Email):
    #    contact = Contact.query.filter_by(Email=Email.data).first()
    #    if contact:
    #        raise ValidationError('That email is taken. Please choose a different one.')
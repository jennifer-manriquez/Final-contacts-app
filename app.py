from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError, Regexp
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1ac8277b9ecb407ce9ef4b5932719b0b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#posts = [
#    {
#        'FirstName': 'Example1',
#        'LastName': 'Example1Last',
#        'Company': 'Example1Encora',
#        'PhoneNumber': '1111111111', 
#        'Email': 'example1@gmail.com', 
#    },
#    {
#        'FirstName': 'Example2',
#        'LastName': 'Example2Last',
#        'Company': 'Example2Encora',
#        'PhoneNumber': '2222222222', 
#        'Email': 'example2@gmail.com', 
#    }
#]

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20), nullable=False)
    LastName = db.Column(db.String(20), nullable=False)
    Company = db.Column(db.String(20))
    PhoneNumber = db.Column(db.String(40)) #Set Unique to true with unique=True
    Email = db.Column(db.String(120), nullable=False) # #Set Unique to true with unique=True

    def __repr__(self):
        return f"Contact('{self.FirstName}', '{self.LastName}', '{self.Company}', '{self.PhoneNumber}', '{self.Email}')"

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

    #def validate_PhoneNumber(self, boo=False):
    #    if boo:
    #        raise ValidationError('That phone number is taken. Please choose a different one.')

    #def validate_PhoneNumber(self, PhoneNumber):
    #    contact = Contact.query.filter_by(PhoneNumber=PhoneNumber.data).first()
    #    if contact:
    #        raise ValidationError('That phone number is taken. Please choose a different one.')

    #def validate_Email(self, Email):
    #    contact = Contact.query.filter_by(Email=Email.data).first()
    #    if contact:
    #        raise ValidationError('That email is taken. Please choose a different one.')


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Contact.query.order_by(Contact.FirstName.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@app.route("/newContact", methods=['GET', 'POST'])
def newContact():
    form = newContactForm()
    if form.validate_on_submit():
        contact = Contact(FirstName=form.FirstName.data, LastName=form.LastName.data, Company=form.Company.data, PhoneNumber=form.PhoneNumber.data, Email=form.Email.data)
        db.session.add(contact)
        db.session.commit()
        flash(f'A new contact has been created for {form.FirstName.data}!', 'success')      
        return redirect(url_for('home'))
    return render_template('newContact.html', title='newContact', form=form, legend='New Post')  

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Contact.query.get_or_404(post_id)
    return render_template('post.html', post=post)  

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Contact.query.get_or_404(post_id)
    form = newContactForm()
    if form.validate_on_submit():
        post.FirstName = form.FirstName.data
        post.LastName = form.LastName.data
        post.Company = form.Company.data
        post.PhoneNumber= form.PhoneNumber.data
        validate_phone = Contact.query.filter(Contact.PhoneNumber==form.PhoneNumber.data).first()
        #print(validate_phone)
        #print(validate_phone.FirstName)
        #print(validate_phone.id)
        #print("Validate_phone type", type(validate_phone.id))
        #print(post_id)
        #print("post_id type", type(post_id))
        #print(validate_phone.PhoneNumber)
        #print(type(validate_phone.PhoneNumber))

        #print(Contact.query.all())
        validate_phone = Contact.query.filter(Contact.PhoneNumber==form.PhoneNumber.data).first()
        #print(post_id != validate_phone.id)
        if post_id != validate_phone.id:
        #    validate_PhoneNumber(True)
        #    raise ValidationError('That phone number is taken. Please choose a different one.')
            #form.PhoneNumber.errors
            flash('That phone number is taken please select other', 'success')
            return render_template('newContact.html', post=post, form=form, legend='Update Post')
        #print(validate_email)
        #print(validate_email.FirstName)
        #print(validate_email.id)
        #print("Validate_email type", type(validate_email.id))
        post.Email = form.Email.data
        validate_email= Contact.query.filter(Contact.Email==form.Email.data).first()
        if post_id != validate_email.id:
            flash('That email is taken please select other', 'success')
            return render_template('newContact.html', post=post, form=form, legend='Update Post')

        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id = post_id))
        
    elif request.method == 'GET':
        form.FirstName.data = post.FirstName
        form.LastName.data = post.LastName
        form.Company.data = post.Company
        form.PhoneNumber.data = post.PhoneNumber
        form.Email.data = post.Email
    return render_template('newContact.html', post=post, form=form, legend='Update Post')
    """
    post = Contact.query.get_or_404(post_id)
    form = newContactForm()
    if request.method == "POST":
        if post.FirstName != form.FirstName.data:
            post.FirstName = form.FirstName.data
            db.session.commit()
        if post.LastName != form.LastName.data:
            post.LastName = form.LastName.data
            db.session.commit()
        if post.Company != form.Company.data:
            post.Company = form.Company.data
            db.session.commit()
        if post.PhoneNumber!= form.PhoneNumber.data:
            post.PhoneNumber= form.PhoneNumber.data
            if not form.validate_on_submit():
                return render_template('newContact.html', post=post, form=form, legend='Update Post')
        else:
            pass 
        if post.Email != form.Email.data:
            post.Email = form.Email.data
            if not form.validate_on_submit():
                return render_template('newContact.html', post=post, form=form, legend='Update Post')
            else:
                flash('Your post has been updated', 'success')
                return redirect(url_for('post', post_id = post_id))
        else: 
            return render_template('newContact.html', post=post, form=form, legend='Update Post')

    elif request.method == 'GET':
        print("This happened")
        form.FirstName.data = post.FirstName
        form.LastName.data =  post.LastName
        form.Company.data =  post.Company
        form.PhoneNumber.data =  post.PhoneNumber
        form.Email.data =  post.Email
        return render_template('newContact.html', post=post, form=form, legend='Update Post')
    else:
        return render_template('newContact.html', post=post, form=form, legend='Update Post')
    """
    """
    contact_to_update = Contact.query.get_or_404(post_id)
    form = newContactForm()
    if request.method == "POST":
        updated_post = {}
        try: 
            updated_post["post_id"] = post_id
            updated_post["FirstName"] = request.form["FirstName"]
            updated_post['LastName'] = request.form['LastName']
            updated_post['Company'] = request.form['Company']
            updated_post['PhoneNumber'] = request.form['PhoneNumber']
            updated_post['Email'] = request.form['Email']

            contact_to_update.FirstName = friend_updated["First"]
            contact_to_update.LastName = friend_updated['Last']
            contact_to_update.PhoneNumber = friend_updated['PhoneNumber']
            contact_to_update.Email = friend_updated['Email']
            contact_to_update.Company = friend_updated['Company']

            db.session.commit()
            return redirect('/home')
        except Exception as error:
            return render_template('newContact.html', post=contact_to_update, form=form, legend='Update Post')
    else:
        return render_template('newContact.html', post=contact_to_update, form=form, legend='Update Post')
        """
    """
           
    
#    if form.validate_on_submit():
#         post.FirstName = form.FirstName.data
#         post.LastName = form.LastName.data
#         post.Company = form.Company.data
#         post.PhoneNumber= form.PhoneNumber.data
#         post.Email = form.Email.data
#         db.session.commit()
#         flash('Your post has been updated', 'success')
#         return redirect(url_for('post', post_id = post.id))
#    elif request.method == 'GET':
#        form.FirstName.data = post.FirstName
#        form.LastName.data = post.LastName
#        form.Company.data = post.Company
#        form.PhoneNumber.data = post.PhoneNumber
#        form.Email.data = post.Email
#    return render_template('newContact.html', post=post, form=form, legend='Update Post')
    """

@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Contact.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
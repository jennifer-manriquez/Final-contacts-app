from flask import Flask, render_template, url_for, flash, redirect
from forms import newContactForm
from flask_sqlalchemy import SQLAlchemy

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


@app.route("/")
@app.route("/home")
def home():
    posts = Contact.query.all()
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


if __name__ == '__main__':
    app.run(debug=True)
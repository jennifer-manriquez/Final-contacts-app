from flask import Flask, render_template, url_for, flash, redirect
from forms import newContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1ac8277b9ecb407ce9ef4b5932719b0b'

posts = [
    {
        'FirstName': 'Example1',
        'LastName': 'Example1Last',
        'Company': 'Example1Encora',
        'PhoneNumber': '1111111111', 
        'Email': 'example1@gmail.com', 
    },
    {
        'FirstName': 'Example2',
        'LastName': 'Example2Last',
        'Company': 'Example2Encora',
        'PhoneNumber': '2222222222', 
        'Email': 'example2@gmail.com', 
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/newContact", methods=['GET', 'POST'])
def newContact():
    form = newContactForm()
    if form.validate_on_submit():
    #    contact = Contact(FirstName=form.FirstName.data, LastName=form.LastName.data, Company=form.Company.data, PhoneNumber=form.PhoneNumber.data, Email=form.Email.data)
    #    db.session.add(contact)
    #    db.session.commit()
        flash(f'A new contact has been created for {form.FirstName.data}!', 'success')      
        return redirect(url_for('home'))
    return render_template('newContact.html', title='newContact', form=form, legend='New Post')    


if __name__ == '__main__':
    app.run(debug=True)
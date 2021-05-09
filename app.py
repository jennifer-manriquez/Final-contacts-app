from flask import Flask, render_template, url_for, flash, redirect, request
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
         post.Email = form.Email.data
         db.session.commit()
         flash('Your post has been updated', 'success')
         return redirect(url_for('post', post_id = post.id))
    elif request.method == 'GET':
        form.FirstName.data = post.FirstName
        form.LastName.data = post.LastName
        form.Company.data = post.Company
        form.PhoneNumber.data = post.PhoneNumber
        form.Email.data = post.Email
    return render_template('newContact.html', post=post, form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Contact.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
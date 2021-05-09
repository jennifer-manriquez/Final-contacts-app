from flask import Flask, render_template, url_for
app = Flask(__name__)

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


@app.route("/newContact")
def about():
    return render_template('newContact.html', title='New Contact')


if __name__ == '__main__':
    app.run(debug=True)
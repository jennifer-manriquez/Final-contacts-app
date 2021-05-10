
# Contacts App

This project is a directory for contact numbers.
The techonolgies used for this project are: Flask (SQLAlchemy, wtforms, and other libraries), it uses Bootstrap for CSS and HTML in the Front, and SQLite for the Back

The requirements this application meets are: 

- Forms validate: name(required, alphabetic less than 20 chars), last name(required, alphabetic less than 20 chars), company (optional, alphanumeric),
phone number (optional, numeric, unique between contacts), email (required, unique between contacts, valid)

- Displays all your contacts with pagination (10 contacts per page).
 
- You can create, update and delte contacts


Special thanks to my mentors, that helped me during this process.

## Authors

- [jennifer manriquez](https://github.com/jennifer-manriquez)


  
## Acknowledgements

 - [CoreyMSchafer's code as reference](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog)
 
## Deployment

App is deployed at https://heroku-contacts-app.herokuapp.com/


  
## Installation 
 
1. Set up a virtual environment (with python3)
2. Install requirements

```bash 
  pip3 install -r requirements.txt
```
3. run with 
```bash 
  python3 app.run
```
    
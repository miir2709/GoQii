from flask import Flask, render_template, url_for, flash, redirect, request, session, abort
from forms import RegistrationForm, LoginForm
# from flask_login import LoginManager
# instance of Flask class
app = Flask(__name__) 
app.config['SECRET_KEY'] = '3f4c4a5de0fa9b6394afd0e9e1c423ad'

posts = [
    {
        'author': 'Mihir Mehta',
        'Date Posted': '21 Sept 2020',
    },
    {
        'author': 'Rahul',
        'Date Posted': '22 Sept 2020',
    }
]

@app.route('/')
@app.route('/home')
# @login_required
def home():
    return render_template('home.html', posts = posts, title = 'Home')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsucessful. Try Again', 'danger')
    return render_template('login.html', title='Login', form=form)    


@app.route('/newPatient')
def newPatient():
    return render_template('newPatient.html', title='Input Data')
    
@app.route('/existingPatient')
def existingPatient():
    return render_template('existingPatient.html', title = 'Input Data')

if __name__ == '__main__':
    app.run(debug=True)
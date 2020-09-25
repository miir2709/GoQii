from flask import Flask, render_template, url_for, flash, redirect, request, session, abort
from flask_mysqldb import MySQL
import MySQLdb.cursors
# from flask_login import LoginManager
# instance of Flask class


app = Flask(__name__) 
app.config['SECRET_KEY'] = '3f4c4a5de0fa9b6394afd0e9e1c423ad'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "goqii"
mysql = MySQL(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')


@app.route('/newPatient',methods=['GET','POST'])
def newPatient():
    if request.method == 'POST':
        device_code = request.form['code']
        gender = request.form['gender']
        age = request.form['age']
        religion = request.form['religion']
        occupation = request.form['occupation']
        date_admission = request.form['date_of_admission']
        date_test = request.form['date_of_test']
        date_device = request.form['date_of_device']
        date_discharge = request.form['date_of_discharge']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO patient VALUES (NULL, %s, %s, %s,%s,%s,%s,%s,%s)', (gender, age, religion,occupation,date_admission,date_test,date_device,date_discharge))
        mysql.connection.commit()
        return redirect(url_for('existingPatient'))
    else:
        return render_template('newPatient.html', title='Input Data')



    
@app.route('/existingPatient')
def existingPatient():
    return render_template('existingPatient.html', title = 'Input Data')


@app.route('/entercode',methods=['GET','POST'])
def entercode():
    if request.method == 'POST':
        code = request.form['dcode']
        print(code)
        return render_template('existingPatient.html', title = 'Input Data')
    else:
        return render_template('inputcode.html', title = 'Input Data')


if __name__ == '__main__':
    app.run(debug=True)
"""This is the main Flask File."""
from flask import Flask, render_template, url_for, flash, g
from flask import redirect, request, session, abort, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import numpy as np
import io
import xlwt
import pymysql
# from flask.ext.security import login_required
from flask_login import login_required, LoginManager
# from functools import wraps
# from flask import g, request, redirect, url_for


# def login_required(f):
#     """F."""
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash("log in with correct credentials")
#             return redirect(url_for('login'))
#     return wrap


app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "0000"
app.config['MYSQL_DB'] = "goqii"
mysql = MySQL(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@app.route('/home')
@login_required
def home():
    """F."""
    return render_template('home.html', title='Home')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    """F."""
    if request.method == 'POST':
        username = (request.form["username"])
        password = (request.form["passwd"])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # print("first line:  "+username+"\n"+password)
        user = cursor.execute(
            f'select * from PERSONS where usernames = "{username}" and \
                passwd = "{password}"')
        # print(user)
        if user > 0:
            user = cursor.fetchall()
            return redirect(url_for('home'))
        else:
            flash("Incorrect Username", "error")
            return render_template('login.html', title='Login')
    else:
        return render_template('login.html', title='Login')


@app.route('/Patient', methods=['GET', 'POST'])
@login_required
def newPatient():
    """Fun for adding a new Patient from the Drive."""
    if request.method == 'POST' and request.form['download'] == '1':
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
        temp = cursor.execute(
            f"SELECT * FROM device WHERE device_id = {device_code}")
        if temp > 0:
            temp = cursor.fetchall()
        if temp == 0:
            cursor.execute('INSERT INTO patient VALUES \
                (NULL, %s, %s, %s,%s,%s,%s,%s,%s)', (
                gender, age, religion, occupation, date_admission, date_test,
                date_device, date_discharge))
            pat_id = cursor.execute(
                'SELECT id FROM patient WHERE id = (SELECT LAST_INSERT_ID())')
            if pat_id > 0:
                pat_id = cursor.fetchall()
            # print("Patient ID", pat_id[0]['id'])
            cursor.execute('INSERT INTO device VALUES (%s, %s)',
                           (device_code, pat_id[0]['id']))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('existingPatient',
                            device_code=device_code))
        else:
            flash("Use different Device Code", "info")
            return render_template("newPatient.html", title='Input Data')
    else:
        return render_template('newPatient.html', title='Input Data')


@app.route('/existingPatient/<device_code>', methods=['GET', 'POST'])
@app.route('/existingPatient', methods=['GET', 'POST'])
@login_required
def existingPatient(device_code):
    """Fun for adding device and hospital data to Existing Patient day-wise."""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    patient = cursor.execute(
        f'SELECT * FROM device WHERE device_id = {device_code}')
    if patient > 0:
        patient = cursor.fetchall()
    # print( patient)
    patient_info = cursor.execute(
        f"SELECT * FROM patient WHERE id = {patient[0]['patient_id']}")
    if patient_info > 0:
        patient_info = cursor.fetchall()
    # print(patient_info)
    flag = 1
    # WRITE CODE
    if request.method == 'POST' and request.form['download'] == '1':
        currentDayNum = request.form['currentDayNum']
        currentDayNum_temp = request.form['currentDayNum']
        currentDate = request.form['currentDate']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        temp = cursor.execute(
            f"SELECT * FROM deviceReading WHERE \
                currentDayNum = {currentDayNum} and deviceId = {device_code}")
        if temp > 0:
            temp = cursor.fetchall()
        # 9 am

        if temp == 0:
            temperature9 = request.form['temperature9']
            pulse9 = request.form['pulse9']
            bpHigh9 = request.form['bpHigh9']
            bpLow9 = request.form['bpLow9']
            spo29 = request.form['spo29']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO deviceReading VALUES \
                (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (
                device_code, currentDayNum, currentDate, temperature9, pulse9,
                bpHigh9, bpLow9, spo29, "9"))
            mysql.connection.commit()

            # 12 pm
            temperature12 = request.form['temperature12']
            pulse12 = request.form['pulse12']
            bpHigh12 = request.form['bpHigh12']
            bpLow12 = request.form['bpLow12']
            spo212 = request.form['spo212']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'INSERT INTO deviceReading \
                    VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)',
                (device_code, currentDayNum, currentDate, temperature12,
                 pulse12, bpHigh12, bpLow12, spo212, "12"))
            mysql.connection.commit()

            # 3 pm
            temperature3 = request.form['temperature3']
            pulse3 = request.form['pulse3']
            bpHigh3 = request.form['bpHigh3']
            bpLow3 = request.form['bpLow3']
            spo23 = request.form['spo23']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO deviceReading \
                VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (
                device_code, currentDayNum, currentDate, temperature3,
                pulse3, bpHigh3, bpLow3, spo23, "3"))
            mysql.connection.commit()

            # 6 pm
            temperature6 = request.form['temperature6']
            pulse6 = request.form['pulse6']
            bpHigh6 = request.form['bpHigh6']
            bpLow6 = request.form['bpLow6']
            spo26 = request.form['spo26']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO deviceReading \
                VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (
                device_code, currentDayNum, currentDate, temperature6, pulse6,
                bpHigh6, bpLow6, spo26, "6"))
            mysql.connection.commit()

            temperature9goqii = request.form['temperature9goqii']
            pulse9goqii = request.form['pulse9goqii']
            bpHigh9goqii = request.form['bpHigh9goqii']
            bpLow9goqii = request.form['bpLow9goqii']
            spo29goqii = request.form['spo29goqii']
            cursorgoqii = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO hospitalReading \
                VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (
                patient[0]['patient_id'], currentDayNum, currentDate,
                temperature9goqii, pulse9goqii, bpHigh9goqii, bpLow9goqii,
                spo29goqii, "9"))
            mysql.connection.commit()

            # 12 pm
            temperature12goqii = request.form['temperature12goqii']
            pulse12goqii = request.form['pulse12goqii']
            bpHigh12goqii = request.form['bpHigh12goqii']
            bpLow12goqii = request.form['bpLow12goqii']
            spo212goqii = request.form['spo212goqii']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO hospitalReading \
                VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (
                patient[0]['patient_id'], currentDayNum, currentDate,
                temperature12goqii, pulse12goqii, bpHigh12goqii, bpLow12goqii,
                spo212goqii, "12"))
            mysql.connection.commit()

            # 3 pm
            temperature3goqii = request.form['temperature3goqii']
            pulse3goqii = request.form['pulse3goqii']
            bpHigh3goqii = request.form['bpHigh3goqii']
            bpLow3goqii = request.form['bpLow3goqii']
            spo23goqii = request.form['spo23goqii']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO hospitalReading \
                VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (
                patient[0]['patient_id'], currentDayNum, currentDate,
                temperature3goqii, pulse3goqii, bpHigh3goqii, bpLow3goqii,
                spo23goqii, "3"))
            mysql.connection.commit()

            # 6 pm
            temperature6goqii = request.form['temperature6goqii']
            pulse6goqii = request.form['pulse6goqii']
            bpHigh6goqii = request.form['bpHigh6goqii']
            bpLow6goqii = request.form['bpLow6goqii']
            spo26goqii = request.form['spo26goqii']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'INSERT INTO hospitalReading \
                    VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)',
                (patient[0]['patient_id'], currentDayNum, currentDate,
                    temperature6goqii, pulse6goqii, bpHigh6goqii, bpLow6goqii,
                    spo26goqii, "6"))
            mysql.connection.commit()
        else:
            flag = 0
    # WRITE CODE ENDS HERE

    # READ CODE STARTS

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    dev = cursor.execute(
        f'SELECT * FROM device WHERE device_id = {device_code}')
    if (dev > 0):
        dev = cursor.fetchall()
    # print(dev)
    devices = cursor.execute(
        f"SELECT * FROM device where patient_id = {dev[0]['patient_id']}")
    if devices > 0:
        devices = cursor.fetchall()
    # print(devices)

    listDevice = []
    for d in devices:
        listDevice.append(d['device_id'])
    listDevice = tuple(listDevice)
    # print(listDevice)

    if len(listDevice) == 1:
        listDevice = listDevice[0]
        # 9 am Read
        deviceReading9 = cursor.execute(
            f"SELECT * FROM deviceReading WHERE deviceId = {listDevice} and \
                timeOfReading = 9 ")
        if deviceReading9 > 0:
            deviceReading9 = cursor.fetchall()
        # 12 pm Read
        deviceReading12 = cursor.execute(
            f'SELECT * FROM deviceReading WHERE deviceId = {listDevice} and \
                timeOfReading = 12 ')
        if deviceReading12 > 0:
            deviceReading12 = cursor.fetchall()
        # 3 pm Read
        deviceReading3 = cursor.execute(
            f'SELECT * FROM deviceReading WHERE deviceId = {listDevice} and \
                timeOfReading = 3 ')
        if deviceReading3 > 0:
            deviceReading3 = cursor.fetchall()
        # 6 pm Read
        deviceReading6 = cursor.execute(
            f'SELECT * FROM deviceReading WHERE deviceId = {listDevice} and \
                timeOfReading = 6 ')
        if deviceReading6 > 0:
            deviceReading6 = cursor.fetchall()

    else:
        # 9 am Read
        deviceReading9 = cursor.execute(
            f"SELECT * FROM deviceReading WHERE deviceId IN {listDevice} and \
                timeOfReading = 9 ")
        if deviceReading9 > 0:
            deviceReading9 = cursor.fetchall()
        # 12 pm Read
        deviceReading12 = cursor.execute(
            f'SELECT * FROM deviceReading WHERE deviceId IN {listDevice} and \
                timeOfReading = 12 ')
        if deviceReading12 > 0:
            deviceReading12 = cursor.fetchall()
        # 3 pm Read
        deviceReading3 = cursor.execute(
            f'SELECT * FROM deviceReading WHERE deviceId IN {listDevice} and \
                timeOfReading = 3 ')
        if deviceReading3 > 0:
            deviceReading3 = cursor.fetchall()
        # 6 pm Read
        deviceReading6 = cursor.execute(
            f'SELECT * FROM deviceReading WHERE deviceId IN {listDevice} and \
                timeOfReading = 6 ')
        if deviceReading6 > 0:
            deviceReading6 = cursor.fetchall()

    # print(deviceReading9)
    hospitalReading9 = cursor.execute(
        f"SELECT * FROM hospitalReading WHERE \
            patientId = {patient[0]['patient_id']} and timeOfReading = 9")
    if hospitalReading9 > 0:
        hospitalReading9 = cursor.fetchall()
    # print(hospitalReading9)

    # 12 pm

    # print(deviceReading9)
    hospitalReading12 = cursor.execute(
        f"SELECT * FROM hospitalReading WHERE \
            patientId = {patient[0]['patient_id']} and timeOfReading = 12 ")
    if hospitalReading12 > 0:
        hospitalReading12 = cursor.fetchall()

    # 3 pm

    # print(f'device reading {deviceReading9}')
    # print(f'type of device reading: {type(deviceReading9)}')
    hospitalReading3 = cursor.execute(
        f"SELECT * FROM hospitalReading WHERE \
            patientId = {patient[0]['patient_id']} and timeOfReading = 3 ")
    if hospitalReading3 > 0:
        hospitalReading3 = cursor.fetchall()

    # 6 pm

    hospitalReading6 = cursor.execute(
        f"SELECT * FROM hospitalReading WHERE \
            patientId = {patient[0]['patient_id']} and timeOfReading = 6 ")
    if hospitalReading6 > 0:
        hospitalReading6 = cursor.fetchall()

    # print the current day number
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    currentDayNum = cursor.execute(
        f"SELECT currentDayNum FROM hospitalReading WHERE \
            patientId = {patient[0]['patient_id']} ")
    if currentDayNum > 0:
        currentDayNum = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    currentDate = cursor.execute(
        f"SELECT currentDate FROM hospitalReading WHERE \
            patientId = {patient[0]['patient_id']} ")
    if currentDate > 0:
        currentDate = cursor.fetchall()
    # print(currentDate)
    cursor.close()
    # print(deviceReading9)
    # print(deviceReading12)
    # print(deviceReading3)
    # print(deviceReading6)
    list1 = []
    l_device = []
    l_hosp = []
    if deviceReading9 != 0:
        for i in range(len(deviceReading9)):
            temp_device = []
            temp_hosp = []
            temp_device.append(deviceReading9[i])
            temp_device.append(deviceReading12[i])
            temp_device.append(deviceReading3[i])
            temp_device.append(deviceReading6[i])

            temp_hosp.append(hospitalReading9[i])
            temp_hosp.append(hospitalReading12[i])
            temp_hosp.append(hospitalReading3[i])
            temp_hosp.append(hospitalReading6[i])

            l_device.append(temp_device)
            l_hosp.append(temp_hosp)
            list1.append(l_device)
            list1.append(l_hosp)

    # print("\nDevice ", l_device)
    # print("\nHospital ", l_hosp)
    # output in bytes
    if request.method == "POST" and request.form['download'] == '3':
        
        output = io.BytesIO()
        # create WorkBook object
        workbook = xlwt.Workbook()
        # add a sheet
        sh = workbook.add_sheet(f'Device {device_code} Report') 
        # add headers
        sh.write(0, 0, 'Device Id')
        sh.write(0, 1, 'Day Number')
        sh.write(0, 2, 'Date')
        sh.write(0, 3, 'Time Of Reading')
        sh.write(0, 4, 'Temperature_Goqii')
        sh.write(0, 5, 'Pulse_Goqii')
        sh.write(0, 6, 'BP High Goqii')
        sh.write(0, 7, 'BP Low Goqii')
        sh.write(0, 8, 'SPO2_Goqii')
        sh.write(0, 9, 'Temperature Hospital')
        sh.write(0, 10, 'Pulse Hopsital')
        sh.write(0, 11, 'BPLOW Hospital')
        sh.write(0, 12, 'BPHIGH Hopsital')
        sh.write(0, 13, 'SPO2 Hospital')
        
        idx = 0
        for device_row, hospital_row in zip(l_device, l_hosp):
            for d_row, h_row in zip(device_row, hospital_row):
                print("Device Row: ",d_row)
                sh.write(idx+1, 0, d_row['deviceId'])
                sh.write(idx+1, 1, d_row['currentDayNum'])
                sh.write(idx+1, 2, d_row['currentDate'])
                sh.write(idx+1, 3, d_row['timeOfReading'])
                sh.write(idx + 1, 4, d_row['temperature'])
                sh.write(idx+1, 5, d_row['pulse'])
                sh.write(idx+1, 6, d_row['bpHigh'])
                sh.write(idx+1, 7, d_row['bpLow'])
                sh.write(idx+1, 8, d_row['spo2'])
                sh.write(idx+1, 9, h_row['temperature'])
                sh.write(idx+1, 10, h_row['pulse'])
                sh.write(idx+1, 11, h_row['bpHigh'])
                sh.write(idx + 1, 12, h_row['bpLow'])
                sh.write(idx + 1, 13, h_row['spo2'])
                idx += 1
        workbook.save(output)
        output.seek(0)
        return Response(output, mimetype="application/ms-excel",
                        headers={"Content-Disposition": f"attachment; \
                            filename=device_{device_code}_report.xls"})

    # print(f'L:  {list1[0][0]}')
    # print(f'L:  {list1[1][0]}')
    # print(deviceReading9[0])
    if flag == 0:
        flash(f"Data for Day Number {currentDayNum_temp} exists", 'info')
        return render_template(
            'existingPatient.html',
            title='Input Data', info=patient_info[0],
            device_code=device_code,
            currentDayNum=currentDayNum, currentDate=currentDate,
            l_device=l_device, l_hosp=l_hosp,
            list1=list1
        )
    else:

        return render_template(
            'existingPatient.html', title='Input Data', info=patient_info[0],
            device_code=device_code, currentDayNum=currentDayNum,
            currentDate=currentDate,
            l_device=l_device, l_hosp=l_hosp,
            list1=list1
            )
# end 13:45


@app.route('/entercode', methods=['GET', 'POST'])
@login_required
def entercode():
    """Fun for entering device Code."""
    if request.method == 'POST':
        if request.form['change_device'] == '0':
            code = request.form['dcode']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            patient = cursor.execute(
                f'SELECT * FROM device WHERE device_id = {code}')
            if patient > 0:
                patient = cursor.fetchall()
            if patient == 0:
                flash("Incorrect Device Code", "error")
                return render_template('inputcode.html', title='Input Data')
            else:
                temp = cursor.execute(
                    f"SELECT device_id FROM device WHERE \
                        patient_id = {patient[0]['patient_id']}")
                if temp > 0:
                    temp = cursor.fetchall()

                if temp[-1]['device_id'] == int(code):
                    # print(patient)
                    patient_info = cursor.execute(
                        f"SELECT * FROM patient WHERE \
                            id = {patient[0]['patient_id']}")
                    if patient_info > 0:
                        patient_info = cursor.fetchall()
                    # print(patient_info)
                    return redirect(url_for(
                        'existingPatient', device_code=code))
                else:
                    flash("Use new device code", "info")
                    return render_template(
                        'inputcode.html', title='Input Data')
        if request.form['change_device'] == '1':
            old_code = request.form['currentDeviceCode']
            new_code = request.form['newDeviceCode']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            patient = cursor.execute(
                f'SELECT * FROM device WHERE device_id = {old_code}')
            if patient > 0:
                patient = cursor.fetchall()
            all_devices = cursor.execute(
                f"SELECT * FROM device WHERE \
                    patient_id = {patient[0]['patient_id']}")
            if all_devices > 0:
                all_devices = cursor.fetchall()
            if all_devices[-1]['device_id'] != int(old_code):
                flash("This device does not exists", "info")
                return render_template("inputcode.html", title='Input Data')
            print("Yes ", patient)
            if patient == 0:
                flash("Enter Correct Device Code", "error")
                return render_template('inputcode.html', title='Input Data')
            temp = cursor.execute(
                f"SELECT * FROM device WHERE device_id = {new_code}")
            if temp > 0:
                temp = cursor.fetchall()
            print(temp)
            if temp != 0:
                flash("Use new device code", "info")
                return render_template('inputcode.html', title='Input Data')
            else:
                cursor.execute("INSERT INTO device VALUES (%s, %s)",
                               (new_code, patient[0]['patient_id']))
                mysql.connection.commit()
                return render_template('inputcode.html', title='Input Data')

    else:
        return render_template('inputcode.html', title='Input Data')


if __name__ == '__main__':
    app.config['SECRET_KEY'] = '3f4c4a5de0fa9b6394afd0e9e1c423ad'
    app.run(debug=True, host='0.0.0.0')

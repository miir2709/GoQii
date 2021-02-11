from flask import Flask, render_template, url_for, flash, g
from flask import redirect, request, session, abort, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import numpy as np
import os
import io
import xlwt
import pymysql
<<<<<<< HEAD
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.stats import ttest_rel, ttest_1samp
# from flask.ext.security import login_required
=======
>>>>>>> 63bb8ba9b256608c350973f3b77beaa431600249
from flask_login import login_required, LoginManager
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "0000"
app.config['MYSQL_DB'] = "goqii"
mysql = MySQL(app)
socketio = SocketIO(app)


@app.route('/home',methods=['GET','POST'])
def home():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    else:
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
                passwd = MD5("{password}")')
        print(user)
        if user > 0:
            user = cursor.fetchall()
            session['loggedin'] = True
            return redirect(url_for('home'))
        else:
            flash("Incorrect Username", "error")
            return render_template('login.html', title='Login')
    else:
        return render_template('login.html', title='Login')


@app.route('/Patient', methods=['GET', 'POST'])
def newPatient():
<<<<<<< HEAD
    """Fun for adding a new Patient from the Drive."""
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
=======
    if not session.get('loggedin'):
        return redirect(url_for('login'))
>>>>>>> 63bb8ba9b256608c350973f3b77beaa431600249
    else:
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
def existingPatient(device_code):
    """Fun for adding device and hospital data to Existing Patient day-wise."""
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    else:
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


@app.route('/plots', methods=['GET'])
def plots():
    """Fun for entering device Code."""
    return render_template('plots.html', title='Plots')


@app.route('/entercode', methods=['GET', 'POST'])
def entercode():
    """Fun for entering device Code."""
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    else:
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


@socketio.on('disconnect')
def disconnect_user():
    session['loggedin'] = False

@app.route("/results", methods=['GET', 'POST'])
def results():
    flag = 0
    if request.method == "POST":
        df = pd.read_csv("Final_Data_Updated_09_02.csv")

        if request.form['result_type'] == 'plot':
            col = request.form['column']
            for filename in os.listdir('static/img'):
                if filename.startswith(f'{col}_'):  # not to remove other images
                    os.remove('static/img/' + filename)
            
            plt.style.use('fivethirtyeight')        
            temp_df = df[[col+'_Goqii', col+'_Hospital', 'Abs_'+col+'_Diff', 'Mean_'+col]]
            temp_df['Mean_'+col] = np.floor(temp_df['Mean_'+col])
            temp_mean = temp_df[['Abs_'+col+'_Diff', 'Mean_'+col]].groupby('Mean_'+col, sort=True, as_index=False).mean()
            plt.figure(figsize=(16, 12))
            plt.plot(temp_mean['Mean_'+col].values, temp_mean['Abs_'+col+'_Diff'].values, marker='o')
            plt.title(f'{col} Vs Mean Absolute {col} Difference', fontsize=30)
            plt.xlabel(f'{col}', fontsize=25)
            plt.ylabel(f"Mean Absolute {col} Difference", fontsize=25)
            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            new_graph_name = col+"_" + str(time.time()) + ".png"
            plt.savefig('static/img/'+ new_graph_name)
            new_graph_name = 'static/img/' + new_graph_name

            fig, (ax1, ax2) = plt.subplots(1,2, figsize=(16, 12))
            temp1 = np.floor(df[col+'_Goqii'])
            ax1.hist(temp1, edgecolor='black', bins=7)
            for p in ax1.patches:
                ax1.annotate(np.round(p.get_height(), decimals=2),
                        (p.get_x()+p.get_width()/2, p.get_height()),
                        ha='center', va='center', xytext=(0,10), textcoords='offset points', fontsize=15)
            ax1.set_xlabel(f'{col}_Goqii', fontsize=25)
            ax1.set_ylabel("Frequency", fontsize=25)
            ax1.set_title("HISTOGRAM", fontsize=30)
            ax1.tick_params(axis="x", labelsize=20)
            ax1.tick_params(axis="y", labelsize=20)
            temp2 = np.floor(df[col+'_Hospital'])
            ax2.hist(temp2, edgecolor='black', bins=7)
            for p in ax2.patches:
                ax2.annotate(np.round(p.get_height(), decimals=2),
                        (p.get_x()+p.get_width()/2, p.get_height()),
                        ha='center', va='center', xytext=(0,10), textcoords='offset points', fontsize=15)
            ax2.set_xlabel(f'{col}_Hospital', fontsize=25)
            ax2.set_ylabel("Frequency", fontsize=25)
            ax2.set_title("HISTOGRAM", fontsize=30)
            ax2.tick_params(axis="x", labelsize=15)
            ax2.tick_params(axis="y", labelsize=15)

            new_graph_name1 = col+"_" + str(time.time()) + ".png"
            plt.savefig('static/img/'+ new_graph_name1)
            new_graph_name1 = 'static/img/' + new_graph_name1

            plt.figure(figsize=(16, 12))
            data1     = np.asarray(temp_df[col+'_Goqii'])
            data2     = np.asarray(temp_df[col+'_Hospital'])
            mean      = np.mean([data1, data2], axis=0)
            diff      = data1 - data2                   # Difference between data1 and data2
            md        = np.mean(diff)                   # Mean of the difference
            sd        = np.std(diff, axis=0)            # Standard deviation of the difference

            plt.scatter(mean, diff)
            plt.axhline(md,           color='gray', linestyle='--')
            plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
            plt.axhline(md - 1.96*sd, color='gray', linestyle='--')            
            plt.xlabel(f"Mean {col}", fontsize=25)
            plt.ylabel(f"{col} Difference", fontsize=25)
            plt.title(f"Bland-Altman - {col}", fontsize=30)
            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            new_graph_name2 = col+"_" + str(time.time()) + ".png"
            plt.savefig('static/img/'+ new_graph_name2)
            new_graph_name2 = 'static/img/' + new_graph_name2
            #return redirect(url_for('graphs'))
            flag = 1
            return render_template('results.html', title="Results", filename1=new_graph_name, filename2=new_graph_name1, filename3=new_graph_name2,flag=flag)
        else:
            col = request.form['column']
            temp = df[col+"_Hospital"]
            meanh = np.mean(temp)
            median = np.median(temp)
            mode = temp.mode()[0]
            std = np.std(temp)
            var = np.var(temp)
            stderr = std/(np.sqrt(len(temp)))
            kurt = temp.kurtosis()
            skew = temp.skew()
            ran = len(temp.unique())
            minimum = temp.min()
            maximum = temp.max()
            add = sum(temp)
            count = len(temp)

            temp1 = df[col+"_Goqii"]
            mean1 = np.mean(temp1)
            median1 = np.median(temp1)
            mode1 = temp1.mode()[0]
            std1 = np.std(temp1)
            var1 = np.var(temp1)
            stderr1 = std/(np.sqrt(len(temp1)))
            kurt1 = temp1.kurtosis()
            skew1 = temp1.skew()
            ran1 = len(temp1.unique())
            minimum1 = temp1.min()
            maximum1 = temp1.max()
            add1 = sum(temp1)
            count1 = len(temp1)

            t_2 = ttest_rel(temp, temp1)[1]
            t_1 = ttest_1samp(temp.values, np.mean(temp1.values))[1]
            flag = 2
            return render_template('results.html', title="Results", flag=flag,
            mean=meanh, median=median, mode=mode, std=std, var=var, stderr=stderr, kurt=kurt, skew=skew, ran=ran, minimum=minimum, maximum=maximum, add=add, count=count, 
            mean1 = mean1, median1 = median1, mode1 =  mode1, std1 = std1, var1 = var1, stderr1 = stderr1, kurt1 = kurt1, skew1 = skew1, ran1 = ran1, minimum1 = minimum1, maximum1 = maximum1,add1 =  add1, count1 = count1,
            t_2 = t_2, t_1 = t_1, col=col
            )
    return render_template('results.html', title="Results", flag=flag)

@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    return render_template('graphs.html', title="Results")

if __name__ == '__main__':
    app.config['SECRET_KEY'] = '3f4c4a5de0fa9b6394afd0e9e1c423ad'
<<<<<<< HEAD
    app.run(debug=True) #host='0.0.0.0')
=======
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)

>>>>>>> 63bb8ba9b256608c350973f3b77beaa431600249

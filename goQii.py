from flask import Flask, render_template, url_for, flash, redirect, request, session, abort
from flask_mysqldb import MySQL
import MySQLdb.cursors
import numpy as np
# from flask_login import LoginManager
# instance of Flask class


app = Flask(__name__) 
app.config['SECRET_KEY'] = '3f4c4a5de0fa9b6394afd0e9e1c423ad'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "0000"
app.config['MYSQL_DB'] = "goqii"
mysql = MySQL(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home')


@app.route('/   Patient',methods=['GET','POST'])
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
        pat_id = cursor.execute('SELECT id FROM patient WHERE id = (SELECT LAST_INSERT_ID())')
        if pat_id > 0:
            pat_id = cursor.fetchall()
        # print("Patient ID", pat_id[0]['id'])
        cursor.execute('INSERT INTO device VALUES (%s, %s)', (device_code, pat_id[0]['id']))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('existingPatient', device_code=device_code))
    else:
        return render_template('newPatient.html', title='Input Data')



    
@app.route('/existingPatient/<device_code>' , methods=['GET','POST'] )
@app.route('/existingPatient', methods=['GET','POST'])
def existingPatient(device_code):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    patient = cursor.execute(f'SELECT * FROM device WHERE device_id = {device_code}')
    if patient > 0:
        patient = cursor.fetchall()
    # print( patient)
    patient_info = cursor.execute(f"SELECT * FROM patient WHERE id = {patient[0]['patient_id']}")
    if patient_info > 0:
        patient_info = cursor.fetchall()
    # print(patient_info)

# 13: 45
    # formid = request.args.get('formid', 1, type=int)
    if request.method == 'POST' :
        currentDayNum = request.form['currentDayNum']
        currentDate = request.form['currentDate']
        
        # 9 am 
        temperature9 = request.form['temperature9']
        pulse9 = request.form['pulse9']
        bpHigh9 = request.form['bpHigh9']
        bpLow9 = request.form['bpLow9']
        spo29 = request.form['spo29']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO deviceReading VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (device_code, currentDayNum, currentDate, temperature9, pulse9, bpHigh9, bpLow9, spo29, "9"))
        mysql.connection.commit()
        
        # 12 pm
        temperature12 = request.form['temperature12']
        pulse12 = request.form['pulse12']
        bpHigh12 = request.form['bpHigh12']
        bpLow12 = request.form['bpLow12']
        spo212 = request.form['spo212']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO deviceReading VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (device_code, currentDayNum, currentDate, temperature12, pulse12, bpHigh12, bpLow12, spo212, "12"))
        mysql.connection.commit()
        
        # 3 pm
        temperature3 = request.form['temperature3']
        pulse3 = request.form['pulse3']
        bpHigh3 = request.form['bpHigh3']
        bpLow3 = request.form['bpLow3']
        spo23 = request.form['spo23']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO deviceReading VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (device_code, currentDayNum, currentDate, temperature3, pulse3, bpHigh3, bpLow3, spo23, "3"))
        mysql.connection.commit()
        
        # 6 pm
        temperature6 = request.form['temperature6']
        pulse6 = request.form['pulse6']
        bpHigh6 = request.form['bpHigh6']
        bpLow6 = request.form['bpLow6']
        spo26 = request.form['spo26']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO deviceReading VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (device_code, currentDayNum, currentDate, temperature6, pulse6, bpHigh6, bpLow6, spo26, "6"))
        mysql.connection.commit()
        
        # if deviceID > 0:
        #     deviceID = cursor.fetchall()
        # print("DeviceID", deviceID[0]['deviceID'])
        # cursor.execute('INSERT INTO device VALUES (%s, %s)', (device_code, deviceID[0]['deviceID']))
        
        # cursor.close()


    # elif request.method == 'POST' :
        # 9 am 
        temperature9goqii = request.form['temperature9goqii']
        pulse9goqii = request.form['pulse9goqii']
        bpHigh9goqii = request.form['bpHigh9goqii']
        bpLow9goqii = request.form['bpLow9goqii']
        spo29goqii = request.form['spo29goqii']
        cursorgoqii = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO hospitalReading VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (patient[0]['patient_id'], currentDayNum, currentDate, temperature9goqii, pulse9goqii, bpHigh9goqii, bpLow9goqii, spo29goqii, "9"))
        mysql.connection.commit()
        
        # 12 pm
        temperature12goqii = request.form['temperature12goqii']
        pulse12goqii = request.form['pulse12goqii']
        bpHigh12goqii = request.form['bpHigh12goqii']
        bpLow12goqii = request.form['bpLow12goqii']
        spo212goqii = request.form['spo212goqii']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO hospitalReading VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (patient[0]['patient_id'], currentDayNum, currentDate, temperature12goqii, pulse12goqii, bpHigh12goqii, bpLow12goqii, spo212goqii, "12"))
        mysql.connection.commit()
        
        # 3 pm
        temperature3goqii = request.form['temperature3goqii']
        pulse3goqii = request.form['pulse3goqii']
        bpHigh3goqii = request.form['bpHigh3goqii']
        bpLow3goqii = request.form['bpLow3goqii']
        spo23goqii = request.form['spo23goqii']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO hospitalReading VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (patient[0]['patient_id'], currentDayNum, currentDate, temperature3goqii, pulse3goqii, bpHigh3goqii, bpLow3goqii, spo23goqii, "3"))
        mysql.connection.commit()
        
        # 6 pm
        temperature6goqii = request.form['temperature6goqii']
        pulse6goqii = request.form['pulse6goqii']
        bpHigh6goqii = request.form['bpHigh6goqii']
        bpLow6goqii = request.form['bpLow6goqii']
        spo26goqii = request.form['spo26goqii']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO hospitalReading VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)', (patient[0]['patient_id'], currentDayNum, currentDate, temperature6goqii, pulse6goqii, bpHigh6goqii, bpLow6goqii, spo26goqii, "6"))
        mysql.connection.commit()
        
        # if deviceID > 0:
        #     deviceID = cursor.fetchall()
        # print("DeviceID", deviceID[0]['deviceID'])
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute(f'INSERT INTO device VALUES (%s, %s)', (device_code, deviceID[0]['deviceID']))

    # lists to pass to html file
    temperaturePass = []

    # 9 am Read
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    deviceReading9 = cursor.execute(f'SELECT * FROM deviceReading WHERE deviceId = {device_code} and timeOfReading = 9 ')
    if deviceReading9 > 0:
        deviceReading9 = cursor.fetchall()
    # for device in deviceReading9:
    #     for key, value in device.items():
    #         # for k in list(device.keys()):
    #         #     if k == 'timeOfReading':
    #         if key == 'spo2':
    #             print(f'device reading {value}')
                #print(device)
    # print(f'type of device reading: {type(deviceReading9[0])}')
    # print(deviceReading9[0])
    

    hospitalReading9 = cursor.execute(f"SELECT * FROM hospitalReading WHERE patientId = {patient[0]['patient_id']} and timeOfReading = 9 ")
    if hospitalReading9 > 0:
        hospitalReading9 = cursor.fetchall()
    # print(hospitalReading9)

    # 12 pm
    deviceReading12 = cursor.execute(f'SELECT * FROM deviceReading WHERE deviceId = {device_code} and timeOfReading = 12 ')
    if deviceReading12 > 0:
        deviceReading12 = cursor.fetchall()
    # print(deviceReading9)
    hospitalReading12 = cursor.execute(f"SELECT * FROM hospitalReading WHERE patientId = {patient[0]['patient_id']} and timeOfReading = 12 ")
    if hospitalReading12 > 0:
        hospitalReading12 = cursor.fetchall()
    
     # 3 pm
    deviceReading3 = cursor.execute(f'SELECT * FROM deviceReading WHERE deviceId = {device_code} and timeOfReading = 3 ')
    if deviceReading3 > 0:
        deviceReading3 = cursor.fetchall()
    # print(f'device reading {deviceReading9}')
    # print(f'type of device reading: {type(deviceReading9)}')
    hospitalReading3 = cursor.execute(f"SELECT * FROM hospitalReading WHERE patientId = {patient[0]['patient_id']} and timeOfReading = 3 ")
    if hospitalReading3 > 0:
        hospitalReading3 = cursor.fetchall()

     # 6 pm
    deviceReading6 = cursor.execute(f'SELECT * FROM deviceReading WHERE deviceId = {device_code} and timeOfReading = 6 ')
    if deviceReading6 > 0:
        deviceReading6 = cursor.fetchall()
      
    hospitalReading6 = cursor.execute(f"SELECT * FROM hospitalReading WHERE patientId = {patient[0]['patient_id']} and timeOfReading = 6 ")
    if hospitalReading6 > 0:
        hospitalReading6 = cursor.fetchall()


    # print the current day number
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    currentDayNum = cursor.execute(f"SELECT currentDayNum FROM hospitalReading WHERE patientId = {patient[0]['patient_id']} ")
    if currentDayNum > 0:
        currentDayNum = cursor.fetchall()

    # uniqueDayNumList = []
    # for i in currentDayNum:
    #     for key in i:
    #     # print(i[key])
    #         uniqueDayNumList.append(i[key])
    #     uniqueDayNumList = np.unique(np.array(uniqueDayNumList))
    

    # uniqueDeviceReadingList = []
    # for i in deviceReading9:
    #         for key in i:
    #             # print(i[key])
    #             uniqueDeviceReadingList.append(i[key])
    #         uniqueDeviceReadingList = np.unique(np.array(uniqueDeviceReadingList))
    #         print(uniqueDeviceReadingList)

    # print(np.unique(x))
    # for i in uniqueDayNumList:
    #     print(i)

    # print(currentDayNum[1])

    # print the current Date
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    currentDate = cursor.execute(f"SELECT currentDate FROM hospitalReading WHERE patientId = {patient[0]['patient_id']} ")
    if currentDate > 0:
        currentDate = cursor.fetchall()
    # print(currentDate)
    cursor.close()

    # if request.method == "POST" :
    #     return render_template('existingPatient.html', title='Input Data', info=patient_info[0],
    #                         device_code=device_code, currentDayNum=currentDayNum[0], currentDate=currentDate[0],
    #                         # uniqueDayNumList = uniqueDayNumList,
    #                         deviceReading9 = deviceReading9, hospitalReading9 = hospitalReading9[0],
    #                         deviceReading12 = deviceReading12[0], hospitalReading12 = hospitalReading12[0],
    #                         deviceReading3 = deviceReading3[0], hospitalReading3 = hospitalReading3[0],
    #                         deviceReading6 = deviceReading6[0], hospitalReading6 = hospitalReading6[0],
    #                         )
    
    list1 = []
    l_device = []
    l_hosp = []
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
    print(f'Device:  {l_device[0]}')
    # print(l_hosp)
    print(f'L:  {list1[0][0]}')
    print(f'L:  {list1[1][0]}')

    # print(deviceReading9[0])

    return render_template('existingPatient.html', title='Input Data', info=patient_info[0],
                            device_code=device_code, currentDayNum=currentDayNum, currentDate=currentDate,
                            l_device = l_device, l_hosp = l_hosp,
                            list1 = list1
                            )
    
# end 13:45

@app.route('/entercode',methods=['GET','POST'])
def entercode():
    if request.method == 'POST':
        code = request.form['dcode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        patient = cursor.execute(f'SELECT * FROM device WHERE device_id = {code}')
        if patient > 0:
            patient = cursor.fetchall()
        # print(patient)
        patient_info = cursor.execute(f"SELECT * FROM patient WHERE id = {patient[0]['patient_id']}")
        if patient_info > 0:
            patient_info = cursor.fetchall()
        # print(patient_info)
        return redirect(url_for('existingPatient',device_code=code))
    else:
        return render_template('inputcode.html', title = 'Input Data')


if __name__ == '__main__':
    app.run(debug=True)
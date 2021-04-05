

from flask import Flask, render_template,  request,redirect,url_for,session
import pandas as pd
# from tensorflow import keras
# from keras.models import load_model
import os
import sqlite3

app = Flask(__name__)
app.secret_key = "asdfghjkl"
app.debug = True
#initializing the model
# MODEL_PATH = "data/model.pkl"
# model = load_model("C:\\Users\\SVR SOLUTIONS\\Desktop\\Uday\\data\\Diabetes_prediction_project.h5")



#Define home route
@app.route("/")
def index():
    if('msg' in request.args):
        messages = request.args['msg'] 
        return render_template("login.html",msg=messages)
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    result = {}
    if 'username' in session:
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * from predictions where mobile = ?",(int(session['mobile']),))
            records = cur.fetchall()
            result['prev'] = records
        return render_template("index.html",result = result)
    else:
        msg = "Please Login"
        return redirect(url_for('index',msg=msg))


@app.route("/authentication",methods=['POST'])
def authentication():
    user = request.form['user']
    passw = request.form['pass']
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * from users where password = ? and username  = ?",(passw,user))
        records = cur.fetchall()
        if(len(records) > 0):
            # print(records)
            session['username'] = request.form['user']
            session['mobile'] = records[0][4]
            return redirect(url_for('dashboard'))
        else:
            msg = "Username or Password is incorrect"
            return redirect(url_for('index',msg=msg))
    return render_template("login.html")
 
@app.route("/insertUser",methods=['POST'])
def insertUser():
    fullname = request.form['fullname']
    mobile = request.form['mobile']
    email = request.form['signupemail']
    username = request.form['signupusername']
    password = request.form['signuppassword']
    print(email,username,password)
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * from users where username = ? and email  = ?",(username,email))
        records = cur.fetchall()
        if(len(records) > 0):
            msg = "User already exists"
            return redirect(url_for('index',msg=msg))
        else:
            cur.execute("INSERT INTO users (fullname, email, username, password,mobile) VALUES (?,?,?,?,?)",(fullname,email,username,password,mobile) )
            con.commit()
    msg = "Please Login"
    return redirect(url_for('index',msg=msg))


 
#Define diagnosis route
@app.route("/diagnosis", methods=['POST'])
def diagnosis():
    name = request.form['name']
    gender = request.form['gender']
    Pregnancies = request.form['Pregnancies']
    Glucose = request.form['Glucose']
    BloodPressure = request.form['BloodPressure']
    SkinThickness = request.form['SkinThickness']
    Insulin = request.form['Insulin']
    BMI = request.form['BMI']
    #DiabetesPedigreeFunction = request.form['DiabetesPedigreeFunction']
    Age = request.form['Age']
    HeartRateVariability = request.form['HeartRateVariability']
    #Predict on the given parameters
   
    
    dict = {'Pregenancies': Pregnancies, 'Glucose': Glucose, 'BloodPressure': BloodPressure,'SkinThickness': SkinThickness,'Insulin': Insulin,'BMI': BMI,'Age':Age,'HeartRateVariability': HeartRateVariability}
    
    # df = pd.DataFrame(dict,index=[0])
    
    # df.to_csv('file1.csv')
    
    # validation = pd.read_csv(".\\file1.csv")
    
    # validation = validation.drop("Unnamed: 0", axis = 1)
    
    
    
    result={}
    # prediction = [round(i[0]) for i in model.predict(validation)]
    
    # #print(prediction[0] == 0)
    # #result=''
    # #Route for result
    # if prediction[0] == 1:
    #     result['msg']="please consult doctor as you haved diabetes"
    # elif prediction[0] == 0:
    #     result['msg']="Congrats! You dont have diabetes."
    print(session['mobile'])
    result['msg'] = "Congrats! You dont have diabetes."
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO predictions (name, gender, Age,Pregnancies, Glucose,BloodPressure,SkinThickness,Insulin,BMI,HeartRateVariability,mobile,result) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(name,gender,Age,Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,HeartRateVariability,session['mobile'],result['msg']) )
        con.commit()
    with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * from predictions where mobile = ?",(int(session['mobile']),))
            records = cur.fetchall()
            result['prev'] = records
   
    
    # print(result)    
    #df.to_csv('file1.csv')
        
    return render_template('index.html', result=result)

        
        
if __name__ == "__main__":
    app.run()

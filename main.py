from unittest import result
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import re
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename



app = Flask(__name__)
#run_with_ngrok(app)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'web-health_project'
app.config['MYSQL_CURSORCLASS']='DictCursor'
app.secret_key = 'MySecretKey'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('dashboard.html') 

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method=='POST':
        #post data 
        email=request.form["email"]
        pwd=request.form["pwd"]
        #sql query
        cur=mysql.connection.cursor()
        cur.execute("select * from users where email=%s and user_pwd=%s",(email,pwd))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['user_id']=data["user_id"]
            session['username']=data["user_name"]
            session['user_role']=data["user_role"]
            flash('Login Sucessfully', 'success')
            return redirect('dashboard')
        else:
            flash('Invalid username or passwprd, Try Again', 'error')
            return redirect(url_for('login'))
    return render_template('login.html') 

@app.route('/logout')
def logout():
    # Remove session data
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.clear()
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'pass' in request.form and 'email' in request.form:
        username = request.form['name']
        surname = request.form['surname']
        password = request.form['pass']
        re_pass = request.form['re_pass']
        email = request.form['email']
        
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', [email])
        account = cur.fetchone()
        if account:
            flash('Email นี้มีผู้ใช้งานแล้ว','error')
            return redirect(url_for('register'))
        if password == re_pass :
            cur.execute('INSERT INTO users(user_name,surname,user_pwd,user_role,email) VALUES (%s, %s, %s, %s,%s)' , (username, surname, password,'member',email))
            mysql.connection.commit()
            cur.execute("select * from users where email=%s and user_pwd=%s",(email,password))
            data=cur.fetchone()
            session['logged_in']=True
            session['user_id']=data["user_id"]
            session['username']=data["user_name"]
            session['user_role']=data["user_role"]
            flash('Login Sucessfully', 'success')
            return redirect('dashboard')
        else:
            flash('กรุณาใส่รหัสผ่านให้ตรง', 'error')
            return redirect(url_for('register'))  
    return render_template('register.html') 

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html') 

@app.route('/user')
def user():
    if not session:
        return redirect('login')
    cur=mysql.connection.cursor()
    cur.execute("select * from users where user_name=%s and user_id=%s",(session['username'],session['user_id']))
    data=cur.fetchone()
    return render_template('user.html',result = {
        "username":data["user_name"],
        "surname":data["surname"],
        "name":data["name"],
        "id_card":data["id_card"],
        "email":data["email"],
        "user_add":data["user_add"],
        "user_prov":data["user_prov"],
        "user_dist":data["user_dist"],
        "user_sub_dist":data["user_sub_dist"],
        "user_zipcode":data["user_zipcode"],
        "user_tel":data["user_tel"]
    }) 
    
@app.route('/user/v1' , methods=['GET', 'POST'])
def user_update():
    if request.method == 'POST':
        username = request.form['user_name']
        email = request.form['email']
        id_card = request.form['id_card']
        user_tel = request.form['user_tel']
        name = request.form['name']
        surname = request.form['surname']
        user_add = request.form['user_add']
        user_prov = request.form['user_prov']
        user_dist = request.form['user_dist']
        user_sub_dist = request.form['user_sub_dist']
        user_zipcode = request.form['user_zipcode']
    cur = mysql.connection.cursor()
    sql_update = "update users set user_name = %s,name = %s,surname = %s,email = %s,id_card = %s, user_tel = %s,user_prov = %s,user_dist = %s,user_add = %s,user_sub_dist = %s,user_zipcode = %s where user_id=%s"
    value = (username,name,surname,email,id_card ,user_tel ,user_prov ,user_dist ,user_add ,user_sub_dist ,user_zipcode ,session['user_id'])
    cur.execute(sql_update,value)
    mysql.connection.commit()
    session['username']=username
    flash('แก้ไขข้อมูลเรียบร้อย','success')
    return redirect(url_for('user'))

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if request.method == 'POST':
        prov = request.form['prov']
        dits = request.form['dits']
        age = request.form['age']
        person = request.form['person']
        gender = request.form['gender']
        flexRadioDefault1 = request.form['flexRadioDefault1']
        flexRadioDefault2 = request.form['flexRadioDefault2']
        flexRadioDefault3 = request.form['flexRadioDefault3']
        flexRadioDefault4 = request.form['flexRadioDefault4']
        list = request.form.getlist('list')
        score = 100
        if score < 50 : 
            flash('คุณไม่มีความเสี่ยง')
        elif score > 80:
            flash('คุณมีความเสี่ยงสูง')
        elif score >= 50:
            flash('คุณมีความเสี่ยงปานกลาง')
    return render_template('evaluate.html')

@app.route('/notify')
def notify():
    if not session:
        return render_template('login.html', message="err")
    cur=mysql.connection.cursor()
    cur.execute("select * from users where user_name=%s and user_id=%s",(session['username'],session['user_id']))
    data=cur.fetchone()
    return render_template('notify.html', result = {
        "username":data["user_name"],
        "surname":data["surname"],
        "name":data["name"],
        "id_card":data["id_card"],
        "email":data["email"],
        "user_add":data["user_add"],
        "user_prov":data["user_prov"],
        "user_dist":data["user_dist"],
        "user_sub_dist":data["user_sub_dist"],
        "user_zipcode":data["user_zipcode"],
        "user_tel":data["user_tel"],
        "status":data["state_report"]
    })

@app.route('/notify/v1' ,methods=['GET', 'POST'])
def submit_notify():
    if request.method == 'POST':
        user_id = request.form['user_id']
        name = request.form['name']
        surname = request.form['surname']
        id_card = request.form['id_card']
        user_tel = request.form['user_tel']
        user_add = request.form['user_add']
        user_prov = request.form['user_prov']
        user_dist = request.form['user_dist']
        user_sub_dist = request.form['user_sub_dist']
        user_zipcode = request.form['user_zipcode']
        doc_covidActive = request.files['doc_covidActive']
        doc_idCard = request.files['doc_idCard']
        filename1 = secure_filename(doc_covidActive.filename)
        filename2 = secure_filename(doc_idCard.filename)
    cur=mysql.connection.cursor()
    value_update = 'pending',filename2,filename1,session['user_id']
    cur.execute("update users set state_report = %s, file_path_idCard=%s , file_path_covActive=%s where user_id=%s", value_update)
    mysql.connection.commit()
    flash('ทำการส่งเอกสารเรียบร้อย','success')
    return redirect(url_for('notify'))

@app.route('/document')
def document():
    return render_template('doc.html')

@app.route('/assistant')
def assist():
    cur=mysql.connection.cursor()
    cur.execute("select * from users")
    data=cur.fetchall()
    return render_template('assist.html' , data=data)

@app.route('/icons')
def icons():
    return render_template('icons.html')

if __name__ == '__main__':
    app.run(debug="on")
    #app.run()
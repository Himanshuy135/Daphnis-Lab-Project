from flask import Flask, render_template, redirect, url_for, session, request
from flask_mysqldb import MySQLdb, MySQL

app = Flask(__name__)

app.secret_key = '1a2b3c4d5e6f'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'HF420@mysql'
app.config['MYSQL_DB'] = 'logindata'
app.config['MYSQL_HOST'] = 'localhost'
db = MySQL(app)

@app.route('/')
def ques():
    return render_template('main_ques.html')

@app.route('/user_signin', methods=['GET', 'POST'])
def userindex():
    msg = ''
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM normal_user_data WHERE User_email = %s AND User_password = %s", (username, password))
            info = cursor.fetchone()
            if info is not None:
                if info['User_email'] == username and info['User_password'] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for('profile'))
            else:
                msg = 'Incorrect Username Password combination,Please Sign Up for new user'
    return render_template('normal_user_sign_in.html', msg=msg)


@app.route('/admin_signin', methods=['GET', 'POST'])
def  adminindex():
    msg = ''
    if request.method == "POST": 
        if 'admin_username' in request.form and 'admin_password' in request.form:
            admin_username = request.form['admin_username']
            admin_password = request.form['admin_password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM admin_data WHERE admin_email = %s AND admin_password = %s", (admin_username, admin_password))
            admininfo = cursor.fetchone()
            if admininfo is not None:
                if admininfo['admin_email'] == admin_username and admininfo['admin_password'] == admin_password:
                    session['loginsuccess'] = True
                    return redirect(url_for('profile'))
                else:
                    msg = 'Incorrect admin username/password!'
    return render_template('admin_sign_in.html', msg=msg)


@app.route('/user_signup', methods=['GET','POST'])
def new_user():
    msg = ''
    if request.method == 'POST':
        if 'one' in request.form and 'two' in request.form and 'three' in request.form:
            user_name = request.form['one']
            user_email = request.form['two']
            user_password = request.form['three']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO normal_user_data(User_name, User_email, User_password) VALUES(%s, %s, %s)", (user_name, user_email, user_password))
            db.connection.commit()
            msg = 'You have successfully registered!'
    return render_template('normal_user_sign_up.html', msg=msg)

@app.route('/new/profile')
def profile():
    if session['loginsuccess'] == True:
        return render_template('profile.html')

@app.route('/new/logout')
def logoutsess():
    session.pop('loginsuccess', None)
    return redirect(url_for('userindex'))

if __name__ == '__main__':
    app.run (debug=True)
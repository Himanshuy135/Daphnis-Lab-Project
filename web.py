from flask import Flask, render_template, redirect, url_for, session, request
from flask_mysqldb import MySQLdb, MySQL

app = Flask(__name__)

app.config['MySQL_HOST'] = 'localhost'
app.config['MySQL_USER'] = 'root'
app.config['MySQL_PASSWORD'] = 'HF420@mysql'
app.config['MySQL_DB'] = 'logindata'
db = MySQL(app)

@app.route('/')
def ques():
    return render_template('normal_user_sign_in.html')

@app.route('/user_signin', methods=['GET,POST'])
def userindex():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM normal_user_data WHERE User_email = %s AND User_password = %s", (username, password))
            info = cursor.fetchone()
            if info is not None:
                if info['email'] == username and info['password'] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for('profile'))
            else:
                return redirect(url_for('userindex')) 
    return render_template('normal_user_sign_in.html')


@app.route('/admin_signin', methods=['GET,POST'])
def  adminindex():
    if request.method == "POST": 
        if 'admin_username' in request.form and 'admin_password' in request.form:
            admin_username = request.form['admin_username']
            admin_password = request.form['admin_password']
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM admin_data WHERE admin_email = %s AND admin_password = %s", (admin_username, admin_password))
            admininfo = cur.fetchone()
            if admininfo is not None:
                if admininfo['admin_email'] == admin_username and admininfo['admin_password'] == admin_password:
                    session['loginsuccess'] = True
                    return redirect(url_for('profile'))
                else:
                    return redirect(url_for('adminindex'))
    return render_template('admin_sign_in.html')


@app.route('/user_signup', methods=['GET,POST'])
def new_user():
    if request.method == 'POST':
        if 'one' in request.form and 'two' in request.form and 'three' in request.form:
            user_name = request.form['one']
            user_email = request.form['two']
            user_password = request.form['three']
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO normal_user_data(User_name, User_email, User_password) VALUES(%s, %s, %s)", (user_name, user_email, user_password))
            db.connection.commit()
            return redirect(url_for('userindex'))
    return render_template('normal_user_sign_up.html')

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
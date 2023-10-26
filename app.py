# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
# import datetime
from datetime import datetime
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'driverdrowsiness'

mysql = MySQL(app)



@app.route('/')
def Index():
    msg = ''
    return render_template('login.html', msg=msg)


@app.route('/new_login')
def new_login():
    msg = ''
    return render_template('new_login.html', msg=msg)

@app.route('/loginform')
def loginform():
    msg = ''
    return render_template('login.html', msg=msg)



@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['role'] = account['role']
            session['email'] = account['email']
            userPrimaryId = account['id']
            username = session['username']

            times = datetime.now().time()
            time = times.strftime('%H:%M:%S')

            current_date = datetime.now().date()
            date = current_date.strftime('%Y-%m-%d')
            # time = 1
            # date = 1


            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO userlog VALUES (NULL, % s, % s, % s, % s)', (userPrimaryId, username, time, date,))
            mysql.connection.commit()

            msg = 'Logged in successfully !'
            return redirect(url_for('users'))

            # if account['username'] == "admin" and account['password'] == "admin":
            #     msg = 'Logged in successfully !'
            #     return redirect(url_for('users'))
            # else:
            #     msg = 'User Login successfully !'
            #     return redirect(url_for('userHome'))


        else:
            msg = 'username or password incorrect !'
            return render_template('login.html', msg=msg)


@app.route('/usersrecord')
def users():
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT  * FROM accounts")
    # data = cur.fetchall()
    # cur.close()
    # return render_template('index.html', accounts=data)
    if not session.get('loggedin'):
        return redirect(url_for('loginform'))
    else:
        if session.get('role') == 1:
            # return render_template('index.html')
            cur = mysql.connection.cursor()
            cur.execute("SELECT  * FROM accounts")
            data = cur.fetchall()
            cur.close()
            return render_template('index.html', accounts=data)
        else:
            # return render_template('single_user.html', accounts=session['username'])
            cur = mysql.connection.cursor()
            cur.execute("SELECT  * FROM userlog WHERE username = % s", (session['username'],))
            data = cur.fetchall()
            cur.close()
            return render_template('userHome.html', accounts=data, user_name = session['username'], user_email = session['email'])


# @app.route('/userHome')
# def userHome():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT  * FROM userlog")
#     data = cur.fetchall()
#     cur.close()
#     return render_template('userHome.html', accounts=data)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('loginform'))
    # session.pop('loggedin', None)
    # session.pop('id', None)
    # session.pop('username', None)
    # return redirect(url_for('loginform'))


@app.route('/user_logs')
def user_logs():
    if session.get('role') == 1:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM userlog")
        data = cur.fetchall()
        cur.close()
        return render_template('User_logs.html', accounts=data, name= session['username'])


@app.route('/registerationForm')
def registerationForm():
    msg = ''
    return render_template('register.html', msg=msg)



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not username or not password or not email:
            msg = 'Please fill out the form!'
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            msg = 'Invalid email address!'
        elif not re.match(r'^[A-Za-z0-9]+$', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            else:
                cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
                mysql.connection.commit()
                msg = 'You have successfully registered!'

    return render_template('register.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=True)

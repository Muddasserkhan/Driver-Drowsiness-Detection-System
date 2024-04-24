from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import re
import bcrypt
from flask_bcrypt import Bcrypt

from wtforms import ValidationError

app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'createdproject'

mysql: MySQL = MySQL(app)

bcrypt = Bcrypt()


@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = {}
    username = request.form.get('username', '')
    email = request.form.get('email', '')
    phone_number = request.form.get('phone_number', '')
    license_number = request.form.get('license_number', '')

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check password length
        if len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'


        # Check if username or email already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        user = cur.fetchone()
        cur.close()

        if user:
            if user[1] == username:
                errors['username'] = 'Username already exists.'
            if user[2] == email:
                errors['email'] = 'Email already exists.'

        if username and username[0].isdigit():
            errors['username'] = 'Username should start with an alphabet.'

        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert new user into the database
        if not errors:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email, password, phone_number, license_number) VALUES (%s, %s, %s, %s, %s)", (username, email, hashed_password, phone_number, license_number))
            mysql.connection.commit()
            cur.close()

            # Process form data
            flash('Registration successful!', 'success')
            return redirect(url_for('register'))

    return render_template('register.html', errors=errors, username=username, email=email, phone_number=phone_number, license_number=license_number)



if __name__ == '__main__':
    app.run(debug=True)

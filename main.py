#!/usr/bin/python
from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Connect to the Sqlite database and get DB Connection
def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

# Create DB Table
def create_db_table():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS users''')
        cur.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("User table created successfully")
        # Insert some data into the table
        cur.execute(
            '''INSERT INTO users (name, email, phone, address, country) VALUES \
            ("Veera Raghava Morkonda", "veeraraghava.morkonda@gamil.com", "9999999999", "Tirupati", "India");''')
        conn.commit()
        print("Dummy users inserted into DB table successfully")
    except:
        print("User table creation failed - Maybe table")
    finally:
        conn.close()

create_db_table()

# Create User
@app.route('/create',  methods = ['POST'])
def create_user():
    # Get the data from the form
    name = request.form['name']
    email = request.form['email'] 
    phone = request.form['phone'] 
    address = request.form['address']  
    country = request.form['country']
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)", (name, email, phone, address, country) )
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for('read_users'))
    
# Read Users
@app.route('/', methods=['GET'])    
def read_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        # convert row objects to dictionary
        for i in rows:
            user = {}
            user["id"] = i["id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            user["address"] = i["address"]
            user["country"] = i["country"]
            users.append(user)
    except:
        users = []
    return render_template('read-users.html', data=users) 
 
# Update User
@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update_user(id):
    if request.method=='POST':
        # Get the data from the form
        id = id
        name = request.form['name']
        email = request.form['email'] 
        phone = request.form['phone'] 
        address = request.form['address']  
        country = request.form['country']
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE id =?", (name, email, phone, address, country, id))
            conn.commit()
        except:
            conn.rollback()
        finally:
            conn.close()
        return redirect(url_for('read_users'))
    else:
        user = {}
        try:
            conn = connect_to_db()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE id = ?", (id,))
            row = cur.fetchone()

            # convert row object to dictionary
            user["id"] = row["id"]
            user["name"] = row["name"]
            user["email"] = row["email"]
            user["phone"] = row["phone"]
            user["address"] = row["address"]
            user["country"] = row["country"]
        except:
            user = {}
        finally:
            conn.close()
        return render_template('update-users.html', user=user)
        

# Delete User
@app.route('/delete/<int:id>')
def delete_user(id):
    message = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE from users WHERE id = ?", (id,))
        conn.commit()
        flash("User deleted successfully")
    except:
        conn.rollback()
        flash("Cannot delete user")
    finally:
        conn.close()

    return redirect(url_for('read_users'))


if __name__ == "__main__":
    #app.debug = True
    #app.run(debug=True)
    app.run(port=8000,host="0.0.0.0")

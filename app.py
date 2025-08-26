from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',      
    'database': 'college'
}


def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100),
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            flash("Login Successful", "success")
            return redirect(url_for('feedback', username=username))
        else:
            flash("Invalid Credentials", "danger")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            conn.close()
            flash("Registered Successfully", "success")
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash("Username already exists", "danger")

    return render_template('register.html')

@app.route('/feedback/<username>', methods=['GET', 'POST'])
def feedback(username):
    if request.method == 'POST':
        message = request.form['message']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (username, message) VALUES (%s, %s)", (username, message))
        conn.commit()
        conn.close()
        flash("Feedback submitted successfully!", "success")

    return render_template('feedback.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)

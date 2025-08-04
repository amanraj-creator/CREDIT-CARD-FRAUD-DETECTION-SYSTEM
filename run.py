 
 
from blockchain import Blockchain
blockchain = Blockchain()  # Step 1: Initialize blockchain

from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify
import sqlite3
import numpy as np
import joblib
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# === EMAIL ALERT SETUP ===
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = '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'  # 🔁 Replace with your SendGrid API key
ALERT_EMAIL = 'fraudalert.notifications@gmail.com'  # 🔁 Replace with the email where you want to receive alerts

def send_email_alert(user, prediction_input):
    message = Mail(
        from_email='iamanraj01@gmail.com',  # 🔁 Replace with a verified sender in SendGrid
        to_emails=ALERT_EMAIL,
        subject='🚨 Fraud Alert Detected!',
        html_content=f"""
        <strong>Suspicious Transaction Detected</strong><br><br>
        <b>User:</b> {user}<br>
        <b>Prediction:</b> Fraudulent Transaction<br>
        <b>Input:</b> {prediction_input}
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print("Error sending email alert:", str(e))

# Load your trained model
model = joblib.load('fraud_model.pkl')

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL)''')
    hashed_pw = generate_password_hash('admin123')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', hashed_pw))
    conn.commit()
    conn.close()

init_db()

# ------------------- Web Routes -------------------

@app.route('/')
def index():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        if c.fetchone():
            flash("Username already exists")
            return redirect('/signup')
        # c.execute("INSERT INTO users (username, password) VALUES (?, ?, ?)", (username, hashed_pw))
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))

        conn.commit()
        conn.close()
        flash("Signup successful! Please login.")
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect('/home')
        else:
            flash("Invalid username or password")
            return redirect('/login')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        flash("Please log in first.")
        return redirect('/login')
    

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [float(request.form[f'feature{i}']) for i in range(1, 30)]
        input_array = np.array([features])
        prediction = model.predict(input_array)
        result = '⚠️ Fraudulent Transaction!' if prediction[0] == 1 else '✅ Legitimate Transaction'

        # 🔗 Add prediction to blockchain
        blockchain.add_block({
            'user': session.get('username', 'anonymous'),
            'input': features,
            'prediction': int(prediction[0])
        })

        # 📧 Send email alert if fraud is detected
        if prediction[0] == 0:
            send_email_alert(session.get('username', 'anonymous'), features)

        return render_template('result.html', prediction_text=result, values=features)
    except:
        return render_template('result.html', prediction_text="❌ Error: Invalid input or missing value.", values=None)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect('/login')
 

# ------------------- REST API Route -------------------

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()

    if not data or not all(f'feature{i}' in data for i in range(1, 30)):
        return jsonify({'error': 'Missing input. You must send feature1 to feature29.'}), 400

    try:
        features = [float(data[f'feature{i}']) for i in range(1, 30)]
        input_array = np.array([features])
        prediction = model.predict(input_array)[0]
       

        # result = 'fraud' if prediction == 1 else 'legit'
        prediction = [1]  # Force fraud for testing
        result = 'fraud' if prediction == 1 else 'legit'

        # 🔗 Add prediction to blockchain
        blockchain.add_block({
            'api_user': 'external',
            'input': features,
            'prediction': int(prediction)
        })

        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
 

# ------------------- Blockchain Viewer -------------------

@app.route('/blockchain')
def view_blockchain():
    return jsonify(blockchain.chain)

@app.route('/blockchain/view')
def view_blockchain_pretty():
    return render_template('blockchain.html', chain=blockchain.chain)
 

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        card_number = request.form['card_number']
        time = request.form['time']
        amount = request.form['amount']
        merchant = request.form['merchant']

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO transactions (card_number, time, amount, merchant) VALUES (?, ?, ?, ?)",
                  (card_number, time, amount, merchant))
        conn.commit()
        conn.close()

        return redirect(url_for('predict'))  # replace 'predict' with your 29-feature form route name

    return render_template('transaction.html')

# ------------------- Run Server -------------------

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from flask_cors import CORS
import random
import time
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


CORS(app)

# Configure the Flask-Mail extension using environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
mail = Mail(app)

# Store OTPs
otp_store = {}

# OTP expiration time in seconds
OTP_EXPIRATION_TIME = 300

def generate_otp():
    """Generates a 6-digit random OTP"""
    return random.randint(100000, 999999)

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request format'}), 400
    
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    otp = generate_otp()
    otp_store[email] = {
        'otp': otp,
        'timestamp': time.time()
    }
    
    try:
        msg = Message('Your OTP Code', recipients=[email])

        # Render the HTML template for the email content
        html_content = render_template('otp_email.html', otp=otp)

        msg.body = f'Your OTP is {otp}. It is valid for 5 minutes.'  # Plain text fallback
        msg.html = html_content  # HTML version of the email

        mail.send(msg)
        return jsonify({'message': 'OTP sent successfully'})
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return jsonify({'error': 'Failed to send OTP via email'}), 500

@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request format'}), 400
    
    email = data.get('email')
    otp_input = data.get('otp')
    
    if not email or not otp_input:
        return jsonify({'error': 'Email and OTP are required'}), 400
    
    otp_data = otp_store.get(email)
    
    if otp_data is None:
        return jsonify({'error': 'No OTP sent to this email'}), 400
    
    if time.time() - otp_data['timestamp'] > OTP_EXPIRATION_TIME:
        return jsonify({'error': 'OTP has expired'}), 400
    
    if otp_data['otp'] == int(otp_input):
        return jsonify({'message': 'OTP validated successfully'})
    else:
        return jsonify({'error': 'Invalid OTP'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
    
print(os.getenv('MAIL_USERNAME'))  # Check if it prints your email
print(os.getenv('MAIL_PASSWORD'))  # Ensure your password is loaded


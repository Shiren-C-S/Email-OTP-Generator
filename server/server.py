from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import random
import time
import os

app = Flask(__name__)

# Enable CORS for all domains and all routes
CORS(app)

# Configure the Flask-Mail extension
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '<ENTER YOUR MAIL>'
app.config['MAIL_PASSWORD'] = '<ENTER YOUR AP SPECIFIC PASSWORD>'
app.config['MAIL_DEFAULT_SENDER'] ='ENTER YOUR DEFAULT SENDER MAIL HERE'
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
        
        # Define the HTML template for the email
        html_content = f'''
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px;">
                    <h2 style="text-align: center; color: #ffa94d;">Verification Code</h2>
                    <p style="font-size: 16px; color: #333333;">
                        Hello,
                    </p>
                    <p style="font-size: 16px; color: #333333;">
                        Your OTP code is:
                    </p>
                    <div style="text-align: center; padding: 15px; background-color: #f9f9f9; border-radius: 8px; margin: 20px 0;">
                        <h1 style="font-size: 36px; color: #ffa94d;">{otp}</h1>
                    </div>
                    <p style="font-size: 16px; color: #333333;">
                        This OTP is valid for 5 minutes. Please do not share it with anyone.
                    </p>
                    <p style="font-size: 16px; color: #333333;">
                        Regards,<br>Digital Fortress
                    </p>
                </div>
            </body>
        </html>
        '''
        
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

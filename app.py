
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder = '.', static_url_path='')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')   

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    correo_suscriptor = data.get('email')

    if not correo_suscriptor:
        return jsonify({'message': 'Missing email'}), 400
    try:
        msg = Message(
            subject=f"Nuevo suscriptor en Aurum: {correo_suscriptor}",
            sender=app.config['MAIL_USERNAME'],
            recipients=['olivovaleria265@gmail.com'] 
        )
        msg.body = f"¡Felicidades! Alguien se ha suscrito a tu newsletter.\nCorreo: {correo_suscriptor}"

        mail.send(msg)
        return jsonify({'message': 'Subscription successful'}), 200
    except Exception as e:
        print(f"error enviando el correo: {e}")
        return jsonify({'message': 'Failed to send email'}), 500 

if __name__ == '__main__':
    app.run(debug=True)

    






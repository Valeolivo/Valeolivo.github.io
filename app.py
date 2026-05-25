
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

@app.route('/contact', methods=['POST'])
def contact():
    # Usamos request.form si el formulario es enviado como 'application/x-www-form-urlencoded'
    # o request.get_json() si prefieres enviarlo vía fetch como JSON. 
    # Usaremos request.form por ser más estándar en formularios HTML.
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    if not all([fullname, email, phone, message]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        msg = Message(
            subject=f"Nuevo mensaje de contacto: {fullname}",
            sender=app.config['MAIL_USERNAME'],
            recipients=['olivovaleria265@gmail.com']
        )
        msg.body = f"""
        Has recibido un nuevo mensaje de contacto:
        
        Nombre: {fullname}
        Email: {email}
        Teléfono: {phone}
        
        Mensaje:
        {message}
        """

        mail.send(msg)
        return jsonify({'message': 'Message sent successfully'}), 200
    except Exception as e:
        print(f"Error enviando el correo: {e}")
        return jsonify({'message': 'Failed to send email'}), 500







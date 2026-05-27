from flask import Flask, request, jsonify, render_template
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

# 1. Enciende la herramienta para leer el archivo .env seguro
load_dotenv() 

# Añadimos template_folder='templates' para que Flask sepa dónde buscar el HTML
app = Flask(__name__, template_folder='templates', static_folder='.', static_url_path='')

@app.route("/")
def inicio():
    # Mantenemos esto igual para cargar la página principal
    return app.send_static_file("index.html")

@app.route("/contact", methods=["POST"])
def enviar_correo():
    # 1. Capturamos los datos
    fullname = request.form.get("fullname")
    correo = request.form.get("email")
    telefono = request.form.get("phone")
    mensaje = request.form.get("message")

    if not all([fullname, correo, telefono, mensaje]):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    # 2. Construcción del correo
    email = EmailMessage()
    
    # Extraemos el correo del remitente de forma segura desde el .env
    correo_remitente = os.getenv("MAIL_USERNAME")
    
    email["From"] = correo_remitente
    email["To"] = "mavale0811@gmail.com"
    email["Subject"] = f"AURUM - Nuevo mensaje de: {fullname}"

    email.set_content(f"""
Nuevo mensaje recibido desde la página web:

Nombre: {fullname}
Correo: {correo}
Teléfono: {telefono}

Mensaje:
{mensaje}
    """)

    # 3. Envío del correo
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            
            # AQUÍ ESTÁ LA MAGIA DE SEGURIDAD: 
            # Python leerá la contraseña sin que esté escrita en el código
            clave_segura = os.getenv("MAIL_PASSWORD")
            smtp.login(correo_remitente, clave_segura)
            
            smtp.send_message(email)
        
        # Si todo sale perfecto, renderizamos tu página estética
        return render_template("success.html", nombre=fullname, correo=correo, telefono=telefono, mensaje=mensaje)

    except Exception as e:
        print(f"Error interno al enviar el correo: {e}")
        
        # PARCHE DE RED: Si el error es el -1 (falsa alarma de desconexión), 
        # asumimos que el correo llegó y mostramos la página de éxito.
        if str(e) == "-1":
            return render_template("success.html", nombre=fullname, correo=correo, telefono=telefono, mensaje=mensaje)
        
        # Si es cualquier otro error real, mostramos la pantalla de error tradicional.
        else:
            return "Hubo un error real al enviar el correo. Intenta de nuevo.", 500

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre = request.form.get("fullname")
        correo = request.form.get("email")
        telefono = request.form.get("phone")
        mensaje = request.form.get("message")
        
        # En lugar de tener el HTML aquí, le pasamos las variables a un archivo HTML externo
        return render_template("success.html", nombre=nombre, correo=correo, telefono=telefono, mensaje=mensaje)

    # Si es GET (cuando el usuario entra a la URL normalmente), mostramos el formulario
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

    








from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage

# Configuramos la carpeta de archivos estáticos para que lea tu index.html y recursos en la misma ruta
app = Flask(__name__, static_folder='.', static_url_path='')

@app.route("/")
def inicio():
    # Usamos send_static_file para mantener tu estructura actual sin necesidad de crear una carpeta "templates"
    return app.send_static_file("index.html")

# La ruta debe llamarse /contact porque así está configurada en tu código JavaScript (fetch)
@app.route("/contact", methods=["POST"])
def enviar_correo():
    # 1. Capturamos exactamente los atributos "name" que definiste en tu HTML
    fullname = request.form.get("fullname")
    correo = request.form.get("email")
    telefono = request.form.get("phone")
    mensaje = request.form.get("message")

    # Validación de seguridad básica
    if not all([fullname, correo, telefono, mensaje]):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    # 2. Construcción del correo
    email = EmailMessage()
    email["From"] = "isabellaescoduq02@gmail.com" # Debes poner el correo desde el que envías
    email["To"] = "olivovaleria265@gmail.com" # El correo de destino que configuraste previamente
    email["Subject"] = f"AURUM - Nuevo mensaje de: {fullname}"

    email.set_content(f"""
Nuevo mensaje recibido desde la página web:

Nombre: {fullname}
Correo: {correo}
Teléfono: {telefono}

Mensaje:
{mensaje}
    """)

    # 3. Conexión al servidor SMTP y envío
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            # Reemplaza con tus credenciales reales (recuerda usar la contraseña de aplicación, no la normal)
            smtp.login("olivovaleria265@gmail.com", "whjv zorn rcts hqje")
            smtp.send_message(email)
        
        # 4. Retornamos un JSON para que el JavaScript pueda leer data.message sin fallar
        return jsonify({"message": "Message sent successfully"}), 200

    except Exception as e:
        print(f"Error interno al enviar el correo: {e}")
        return jsonify({"message": "Error al enviar el correo. Intenta de nuevo."}), 500

# Bloque obligatorio para que el servidor de desarrollo se mantenga activo
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    







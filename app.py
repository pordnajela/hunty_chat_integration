# Libería utilizada para cargar las variables de entorno
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from webhook import webhook_bp
from messages import messages_bp

def create_app():
    app = Flask(__name__)
    
    # Uso de bluepritns para separar funcionalidades
    app.register_blueprint(webhook_bp)
    app.register_blueprint(messages_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5002)
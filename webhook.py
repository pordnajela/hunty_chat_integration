from flask import Blueprint, request, jsonify
from utils import send_message, chat, insert_message
import os
import hashlib

webhook_bp = Blueprint('webhook', __name__)

# Endpoint que recibe peticiones GET cuando se intenta sincronizar el Backend con la API de Facebook
@webhook_bp.route('/webhook/', methods=['GET'])
def webhook_get():
    # Se debe validar si el TOKEN establecido en la API de Facebook es el mismo que el que se tiene desde Backend
    # Si es correcto se devuelve el challenge
    # Sino Otro mensaje rando, en este caso sería "Webhook Error"
    if request.args.get('hub.verify_token') == os.getenv('WHATSAPP_WEBHOOK_TOKEN_VERIFICATION'):
        return request.args.get('hub.challenge')
    else:
        return "Webhook Error"

# Endpoint que recibe peticiónes POST desde la API de Facebook
@webhook_bp.route('/webhook/', methods=['POST'])
def webhook():
    # Obtengo todo el payload de la petición para después separar los datos de interés y 
    # almacenar el mensaje en la base de datos así como retornar un mensaje del Bot
    whatsapp_data = request.get_json()
    try:
        if whatsapp_data['entry'][0]['changes'][0]['value']['messages'][0]['id']:
            recipient_phone_number = whatsapp_data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            recipient_body = whatsapp_data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

            # Obtengo el mensaje generado por el Bot
            message_to_send = chat(recipient_body)

            # Uso el Sha256 del número del destinatario + el mensaje del destinatario + el mensaje del Bot
            # para crear un hash y tener el ID del mensaje como tal
            message_id = hashlib.sha256((recipient_phone_number+recipient_body+message_to_send).encode('utf-8')).hexdigest()
            
            # Almacenar el mensaje
            insert_message({
                "user_id": recipient_phone_number,
                'user_message': recipient_body,
                'message_id': message_id,
                'bot_message': message_to_send
            })
            
            # Enviar respuesta
            send_message(message_to_send, recipient_phone_number)
            
    except Exception as e:
        print("Exception: " + str(e))
        pass
    return jsonify({"status": "success"}, 200)

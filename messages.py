from flask import Blueprint, request, jsonify
from utils import collection
from utils import chat, insert_message
import hashlib

messages_bp = Blueprint('messages', __name__)

# Enpoint que permite objeter todos los mensajes de todos los usuario
# que han estado enviado mensajes al backend
# [GET] http://127.0.0.1:5002/messages/
@messages_bp.route('/messages/', methods=['GET'])
def all_messages():
    # Consulta a la base de datos para obtener todos los records
    records = collection.find({})
    response = []

    for record in records:
        response.append({
            'user_id': record['user_id'],
            'user_message': record['user_message'],
            'message_id': record['message_id'],
            'bot_message': record['bot_message']
        })

    return jsonify(response)

# Enpoint que permite recibir peticiones POST cuando se desee enviar un mensaje desde el backend
# [POST] http://127.0.0.1:5002/messages/
# Body: { "message": "me puedes recomendar una serie de terror?" }
@messages_bp.route('/messages/', methods=['POST'])
def messages():
    data = request.get_json()
    message_to_send = chat(data['message'])
    recipient_body = data['message']

    # El 'user_id' en este caso lo identifico como 'from_endpoint' ya que no provee ningún número telefónico
    user_id = 'from_endpoint'
    message_id = hashlib.sha256((user_id+recipient_body+message_to_send).encode('utf-8')).hexdigest()

    database_payload = {
        "user_id": user_id,
        'user_message': recipient_body,
        'message_id': message_id,
        'bot_message': message_to_send
    }

    # Se hace una copia del directorio 'database_payload' para que no responda con '_id' que viene desde Mongo
    response = dict(database_payload)

    insert_message(database_payload)

    return jsonify(response)

# Enpoint que permite recibir peticiones GET que por medio del 'message_id' se puede obtener 
# la información del mensaje desde la base de datos
# [GET] http://127.0.0.1:5002/messages/bc9fdb602bb82d0aa805a90888d89d2c27e2715fdf68e66231776c40a051e59a
@messages_bp.route('/messages/<message_id>/', methods=['GET'])
def message_by_id(message_id):
    # Consulta que permite traer solamente 1 mensaje desde la base de datos
    record = collection.find_one({'message_id': message_id})
    response = {
        'user_id': record['user_id'],
        'user_message': record['user_message'],
        'message_id': record['message_id'],
        'bot_message': record['bot_message']
    }
    return jsonify(response)

# Enpoint que permite recibir peticiones GET que por medio del 'user_id' se puede obtener 
# la información del mensaje desde la base de datos de dicho usuario
# En este caso cambié el endpoint como decía en la guía de '/messages/{user_id}:' a '/user/<user_id>/messages'
# Para que tuviera un aspecto más RESTful
# [GET] http://127.0.0.1:5002/user/573193206969/messages
@messages_bp.route('/user/<user_id>/messages', methods=['GET'])
def user_message_by_id(user_id):
    # Consulta que permite traer los mensajes asociados al 'user_id' dado.
    records = collection.find({'user_id': user_id})
    response = []

    for record in records:
        response.append({
            'user_id': record['user_id'],
            'user_message': record['user_message']
        })
    return jsonify(response)

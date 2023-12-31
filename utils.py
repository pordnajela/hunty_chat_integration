from pymongo import MongoClient
from heyoo import WhatsApp
import openai
import os

# Instancio el cliente de MongoDB
client = MongoClient(os.getenv('MONGODB_URL'))
db = client['hunty']
collection = db['messages']

# Establezco el TOKEN de OpenAI para poder generar respuesta y enviar mensajes
openai.api_key = os.getenv('OPEN_AI_TOKEN')

def chat(message):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages = [ {'role': 'user', 'content': message}],
        temperature=0.7,
        max_tokens=250
    )
    reply = response.choices[0]['message']['content'].strip()

    return reply

def send_message(msg, recipient_phone_number=os.getenv('WHATSAPP_NUMBER_RECIPIENT')):
    # Se hace uso de la librería heyoo para poder usar el objeto/tipo WhatsApp para
    # el envío de mensajes desde el backend
    whatsapp_client = WhatsApp(os.getenv('WHATSAPP_TOKEN'),os.getenv('WHATSAPP_NUMBER'))
    whatsapp_client.send_message(msg, recipient_phone_number)

def insert_message(message):
    collection.insert_one(message)
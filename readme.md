# Hunty prueba técnica Chat integration

## Introduction

Esta es el desarrollo de un Backend hecho en Flask para la prueba técnica de Hunty Chat Integration que consiste en la integración de Whatsapp Cloud API conectado a una base de datos MongoDB

### Por qué Flask?
Se utilizó Flask porque es un "micro" web framework que se enfoca en la simplicidad y por el poco tiempo de desarrollo que toma en poder crear endpoints RESTful

### Por qué MongoDB como base de datos NoSQL?
MongoDB es una base de datos NoSQL orientada a documentos, lo cual no necesita de un schema predefinido para almacenar los datos en formato JSON, esto le agrega una gran ventaja en cuanto a la flexibilidad ya que la estructura puede ser cambiante.

## Installation

### Facebook developer account
Crear cuenta como developer en Fcebook para poder obtener los tokens de Whatsapp. Puede miar el paso a paso en la documentación original [set up developer assets](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started#set-up-developer-assets)

### OpenAI developer account
Crear ua cuenta de desarrollo en OpenAI para configurar el Bot que va a responder los mensajes de Whatsapp siguiendo este tutorial [How to setup and create an OpenAi account and get an API key](https://promptmuse.com/how-to-create-and-openai-account-and-get-an-api/)

### Environment variables
Una vez tengamos ambas cuentas creadas podemos crear el archivo .env el cual contendrá las variables de entorno, para eso ejecutamos el siguiente comando:

```bash
copy .env.example .emv
```

### Docker
El proyecto está Dockerizado por lo que solamente es necesario tener docker instalado y ejecutar el siguiente comand:

```bash
docker-compose up 
```

En este punto ya podemos hacer uso de la aplicación.

## Usage

El proyecto no está para ser desplegado a production por lo que es necesario tener una herramienta que permita crear túneles seguros desde internet hasta la máquina local, por lo cual. Esto nos permite enlazar el webhook de Whatsapp con nuestra aplicación local.

En este caso utilizaremos Ngrok para tal fin, en este link se puede seguir el paso a paso para generar el token y hacer que funcione [Getting Started with ngrok
](https://ngrok.com/docs/getting-started/)

Una vez con Ngrok configurado procedemos a ejecutar el siguiente comando:

```bash
ngrok http 5002
```

Esto nos arrojará los siguientes datos:

```bash
Send your ngrok traffic logs to Datadog: https://ngrok.com/blog-post/datadog-logs

Session Status                online                                                                                                                                      
Account                       Santiago Alejandro Pérez Solarte (Plan: Free)                                                                                                
Version                       3.3.1
Region                        United States (us)
Latency                       102ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://5cae-186-80-126-30.ngrok-free.app -> http://localhost:5002
                               
Connections                   ttl     opn     rt1     rt5     p50     p90                                                                                                                                                                                     
                              135     0       0.00    0.00    0.02    4.20  
```

Ahora tenemos un dominio seguro y gratuito para poder usar en cualquier cliente mediante la siguiente URL *https://5cae-186-80-126-30.ngrok-free.app*.

**NOTA: ESTO ES UN EJEMPLO, EN CADA CASO PUEDE VARIAR LA URL.**

## Postman example requests
En el folder  **documentation** se encuentra el archivo **Hunty_chat_integration.postman_collection.json** que se puede importar directamente en postman para tener una collection con los requests que acepta el proyecto. Aquñi está el link de cómo importar una collection [Importing and exporting data
](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-data-into-postman)
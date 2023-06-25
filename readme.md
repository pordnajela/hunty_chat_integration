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

### Database
Para este proyecto usamos la base de datos MongoDB y para mayor facilidad vamos a usar un contenedor de docker para este fin.

Bajar la imagen de MongoDB
```bash
docker pull mongo
```

Luego crear el contenedor
```bash
docker run --name mymongo -v ./data:/data/db -p 27017:27017 -d mongo
```

Para asegurarnos que el contenedor está corriendo como debe ser ejecutamos los siguientes comandos:

```bash
docker ps -a

CONTAINER ID   IMAGE     COMMAND                  CREATED       STATUS       PORTS                      NAMES
f7b743378988   mongo     "docker-entrypoint.s…"   5 hours ago   Up 5 hours   0.0.0.0:27017->27017/tcp   mymongo

docker exec -it f7b743378988 mongosh

Current Mongosh Log ID:	6498ac4ee8e1f760e8d60910
Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.0
Using MongoDB:		6.0.6
Using Mongosh:		1.10.0

For mongosh info see: https://docs.mongodb.com/mongodb-shell/

------
   The server generated these startup warnings when booting
   2023-06-25T16:19:25.642+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2023-06-25T16:19:26.086+00:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
   2023-06-25T16:19:26.086+00:00: vm.max_map_count is too low
------

test>

```

En este punto ya tenemos el docker listo para las pruebas.

### Python libraries

Instalamos las librerías del proyecto con el siguiente comando:

```bash
pip3 install -r requirements.txt
```

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

Finalmente ejecutamos nuestro Backend con el siguiente comando:

```bash
python3 app.py
```

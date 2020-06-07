## MEAL DELIVERY APP

[![build status](https://github.com/josseed/backend-test-zuniga/workflows/Django-CI/badge.svg)](https://github.com/josseed/backend-test-zuniga/actions) [![build status](https://github.com/josseed/backend-test-zuniga/workflows/Angular-CI/badge.svg)](https://github.com/josseed/backend-test-zuniga/actions) ![Alt text](./backend/coverage.svg)

Esta aplicación permite preguntarle a los usuarios de un workspace de slack que tipo de comida desean y visualizar sus pedidos.

Todo esto gracias a un bot que permite la interacción con tu workspace!

Desarrollado con Django como backend y Angular en el frontend. Enjoy :)

## Configuración del ambiente ##
Es necesario tener instalado npm, python, pip, ngrok, docker y docker-compose para seguir estos pasos.

Las herramientas descritas son fáciles de encontrar en la web, por lo que si no las tienes, las puedes instalar siguiendo los tutoriales de las paginas oficiales.

Este codigo esta testeado para python 3.6, 3.7 y 3.8 por lo cual se recomienda trabajar con estás versiones.

Para levantar las bases de datos necesarias utilizaremos el archivo docker-compose.yml.
El cual contiene una base de datos Redis, Postgres y PGadmin como visualizador de postres, tambíen posee las credenciales de estas tecnologías.
```
docker-compose up -d
```

Instalamos las librerias del backend (es recomendable tener un gestor de ambientes para python):

```
cd backend
pip install -r requirements.txt
```

Instalamos las librerias del frontend:

```
cd frontend
npm i
```


## Configuraciones backend ##
Si vas a usar bds distintas, configura el archivo:
app/settings/develop.py

```
python backend/manage.py makemigrations
python backend/manage.py migrate
python backend/manage.py createsuperuser
```

## Configuración bot slack ##
Primero debes crear una app de slack en el siguiente link: [Crear slack app](https://api.slack.com/apps?new_app=1)

Luego lo debes invitar a tu workspace de testing con con los siguientes permisos:
* chat:write
* im:history
* im:write
* users:read


Modifica las siguientes configuraciones con tu propia app de slack:
```
CLIENT_ID = [your-id]
CLIENT_SECRET = [your-secret]
VERIFICATION_TOKEN =  [your-verification-token]
BOT_USER_ACCESS_TOKEN = [your-bot-user-access-token]
```

Configura el bot a tu gusto con las siguientes configuraciones:

```
AVAILABLE_START_HOUR = 8
AVAILABLE_END_HOUR = 11
TIME_ZONE_BOT = 'America/Santiago'
```
Estas configuraciones se encuentran en backend/app/settings/develop.py

## Para testear el backend ##
```
cd backend
python manage.py test
```

## Para levantar el backend ##
necesitamos dos terminales para esto.
```
cd backend
python manage.py runserver  # en una terminal
celery -A app worker -l info -P gevent # windows
celery -A app worker -l info -B # linux
```

## Para levantar el frontend ##
```
cd frontend
ng serve
```

## para levantar ngrok ##

```
cd 'path-ngrok'
./ngork http 8000
```

## configurar el webhook del bot para que puedas recibir los mensajes de slack ##

Este es el ultimo paso, dado que el webhook de slack solo funciona con https(para eso ngrok).

Dirigete a https://api.slack.com/apps/'tu-app-id'/event-subscriptions?

Activa los eventos y agrega la url correspondiente. 

EJ: https://883379003fb5.ngrok.io/actions/event/hook/

Reemplazar los numeros que te entrega ngrok.

Espera que se valide y subscribe un evento del bot con los siguientes permisos:
* message.im



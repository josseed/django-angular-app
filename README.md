## MEAL DELIVERY APP

[![build status](https://github.com/josseed/backend-test-zuniga/workflows/Django-CI/badge.svg)](https://github.com/josseed/backend-test-zuniga/actions) [![build status](https://github.com/josseed/backend-test-zuniga/workflows/Angular-CI/badge.svg)](https://github.com/josseed/backend-test-zuniga/actions)

Esta aplicación permite preguntarle a los usuarios de un workspace de slack que tipo de comida desean.


## Configuración bot slack ##
Primero deves crear una app de slack en el siguiente link: [Crear slack app](https://api.slack.com/apps?new_app=1)
Lo invitas a tu workspace con con los siguientes permisos:
* chat:write
* im:history
* im:write
* users:read


Modifica los siguientes settings:
CLIENT_ID = [your-id]
CLIENT_SECRET = [your-secret]
VERIFICATION_TOKEN =  [your-verification-token]
BOT_USER_ACCESS_TOKEN = [your-bot-user-access-token]

## Configuramos el ambiente ##



## Configuraciones backend ##
Este codigo esta testeado para python 3.8 por lo cual se recomienda mantener la versión.

Instalamos las librerias:
pip install -r backend/requirements.txt






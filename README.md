# QuienSumaApp
"Quien Suma" es una aplicación web diseñada para conectar equipos de fútbol que necesitan jugadores con aficionados apasionados por el deporte que desean unirse a un equipo o jugar ocasionalmente. La aplicación simplifica la coordinación, la comunicación y la organización de partidos, mejorando la experiencia de la comunidad futbolística.

El proyecto "Quien Suma" representa una iniciativa innovadora destinada a abordar desafíos comunes en el ámbito del fútbol amateur y aficionado. Esta aplicación web tiene como objetivo principal conectar equipos de fútbol que necesitan jugadores adicionales con individuos apasionados por el deporte que desean unirse a un equipo o simplemente disfrutar de un partido ocasional.

El problema:
El mundo del fútbol aficionado enfrenta desafíos significativos, desde la dificultad de encontrar jugadores disponibles para completar un equipo hasta la ineficiente coordinación de partidos y eventos. Esto a menudo conduce a partidos cancelados y experiencias insatisfactorias para los amantes del deporte.

La Solución:
"Quien Suma" es una aplicación web innovadora diseñada para abordar estos problemas. Conecta equipos de fútbol que necesitan jugadores adicionales con individuos apasionados por el deporte que desean unirse a un equipo o jugar partidos. La aplicación ofrecerá un conjunto de funcionalidades clave, que incluyen registro de usuarios, organización de partidos, visualización de partidos próximos, comunicación entre perfiles de usuario, búsqueda de partidos disponibles y una integración con Google Maps para mostrar ubicaciones de partidos.

Alcance del Proyecto:
El alcance del proyecto abarca el desarrollo de la aplicación web, la configuración de la base de datos, la integración de Google Maps y la creación de documentación técnica y de usuario.

Beneficios Esperados:
Facilitar la organización de partidos de fútbol.
Fomentar la participación y la unión en la comunidad deportiva.
Mejorar la experiencia de los usuarios al simplificar la búsqueda y la coordinación de partidos.
Utilizar tecnología avanzada para brindar una plataforma segura y eficiente.

**Objetivos del proyecto**
Diseñar y construir una plataforma de software que sea capaz de gestionar de manera eficiente la coordinación y participación en partidos de fútbol, y que permita:
  Registrar Cuentas de Usuario
  Organizar partidos de futbol
  Unirse a partidos disponibles
  Visualizar partidos disponibles y próximos
  Communication entre perfiles de usuario
  Integration con google maps para mostrar ubicaciones de partidos

Para descargar y usar la aplicación "QuienSumaApp", sigue estos pasos detallados:

# Requisitos Previos
Asegúrate de tener instalados los siguientes componentes antes de comenzar:

* Python 3.11
* PostgreSQL
* Redis: Un almacén de estructuras de datos en memoria, usado para gestionar las notificaciones y mensajes en tiempo real.
  
# Descarga de la Aplicación desde GitHub
Clona el repositorio de la aplicación desde GitHub

git clone https://github.com/chiaradigii/QuienSumaApp.git
cd QuienSumaApp

# Instalación de Dependencias
Asegúrate de activar un entorno virtual (puedes usar venv o virtualenv) para evitar conflictos con otras instalaciones de Python. Luego, instala las dependencias necesarias especificadas en el archivo requirements.txt.

pip install -r requirements.txt

# Configuración de la Base de Datos PostgreSQL
Crea una base de datos en PostgreSQL y configura los detalles en el archivo settings.py de tu proyecto Django. Asegúrate de que la base de datos esté activa y accesible.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_de_tu_base_de_datos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Luego, realiza las migraciones necesarias para configurar la base de datos:

python manage.py migrate

# Ejecución del Servidor Redis
Redis es necesario para gestionar las notificaciones y mensajes.

redis-server

# Ejecución de la Aplicación Localmente
Para correr la aplicación en tu máquina local, usa Daphne. Esto levantará el servidor ASGI necesario para aplicaciones Django en tiempo real.

daphne -p 8000 web_project.asgi:application

# Acceso a la Aplicación
Ahora puedes acceder a la aplicación en tu navegador web visitando http://127.0.0.1:8000.


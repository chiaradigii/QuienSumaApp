# QuienSumaApp
"Quien Suma" is a web application designed to connect soccer teams in need of players with sports enthusiasts looking to join a team or play occasionally. The app simplifies coordination, communication, and match organization, enhancing the experience for the soccer community.

## Overview
The "Quien Suma" project is an innovative initiative aimed at addressing common challenges in the amateur and recreational soccer world. Its primary goal is to connect soccer teams needing additional players with individuals passionate about the sport, whether they want to join a team or simply enjoy an occasional match.

## The Problem
Amateur soccer faces significant challenges, such as:
* Difficulty finding available players to complete a team.
* Inefficient coordination of matches and events.
* Frequent cancellations and unsatisfactory experiences for soccer enthusiasts

## The Solution
"Quien Suma" is a web application designed to tackle these problems by connecting soccer teams with players. The app provides key features such as:
* User registration.
* Match organization.
* Viewing upcoming matches.
* Communication between user profiles.
* Searching for available matches.
* Google Maps integration to display match locations.

## Project Scope
The project includes:
* Developing the web application.
* Setting up the database.
* Integrating Google Maps and other APIs
* Creating technical and user documentation.

**Objetivos del proyecto**
Develop and implement a software platform capable of efficiently managing soccer match coordination and participation, with the following functionalities:
* User account registration.
* Organizing soccer matches.
* Joining available matches.
* Viewing upcoming matches.
* Communication between user profiles.
* Google Maps integration for match locations.

# Installation and Usage Instructions
To download and use the "QuienSumaApp", follow these detailed steps:

## Prerequisites
Asegúrate de tener instalados los siguientes componentes antes de comenzar:

* Python 3.11
* PostgreSQL

## Downloading the Application from GitHub

Clone the application's repository from GitHub:

git clone https://github.com/chiaradigii/QuienSumaApp.git
cd QuienSumaApp

## Installing Dependencies

1. Activate a virtual environment (Optional) 
2. Install the required dependencies listed in the requirements.txt file:

pip install -r requirements.txt

## Configuring the PostgreSQL Database
Create a PostgreSQL database and configure the details in the settings.py file of your Django project. Ensure the database is active and accessible:


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


## Run the necessary migrations to set up the database:

python manage.py migrate

## Running the Redis Server
Redis is required to manage notifications and messaging. Start the Redis server:

redis-server

## Running the Application Locally
To run the application locally, use Daphne. This starts the ASGI server required for real-time Django applications:

daphne -p 8000 web_project.asgi:application

## Accessing the Application 
You can now access the application in your web browser by visiting:
http://127.0.0.1:8000.


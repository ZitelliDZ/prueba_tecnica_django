# Prueba Técnica Django 

* El proyecto incluye una carpeta Postman con un archivo para importar.
* Consta de una aplicación principal llamada Core y otra llamada Redirect.
* El archivo docker-compose define 4 contenedores: DB - DBTest - Cache - Backend (Aplicación).

## Getting Started

1. Correr "docker-compose up" en la terminal.
2. Una vez creados los contenedores, refrescar el contenedor Backend.
3. Correr "docker-compose exec backend sh" en la terminal.
4. Realiza las migraciones con "python manage.py migrate".
5. Crea un usuario administrador con "python manage.py createsuperuser".

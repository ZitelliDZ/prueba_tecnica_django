# Prueba Técnica Django 

* El proyecto incluye una carpeta Postman con un archivo para importar.
* Consta de una aplicación principal llamada Core y una aplicación llamada Redirect.
* El archivo docker-compose define 4 contenedores: DB - DBTest - Cache - Backend (Aplicación).

El documento .docx se encuentra detalles de la prueba.

## Getting Started

1. Correr "docker-compose up" en la terminal.
2. Una vez creados los contenedores, refrescar el contenedor Backend.
3. Correr "docker-compose exec backend sh" en la terminal.
4. Realiza las migraciones con "python manage.py migrate".
5. Crea un usuario administrador con "python manage.py createsuperuser".
6. Correr las pruebas "pytest -W ignore ./redirects/tests/test_redirects.py -v ".
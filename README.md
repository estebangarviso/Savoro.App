# Savoro.App

## Guía de Inicio Rápido

1. Crear entorno virtual `pipenv shell`
2. Instalar dependecias: `pipenv install`
3. Realizar migraciones `python manage.py makemigrations && python manage.py migrate`
4. Ejecutar comando de creación de superusuario `python manage.py createsuperuser`
   1. Ingresar nombre de usuario, correo y contraseña
5. Ejecutar semilla de datos iniciales `python manage.py seed_data`
6. Formatear código `black .`
7. Correr servidor `python manage.py runserver`

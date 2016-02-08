from fabric.api import run, local, hosts, cd
from fabric.contrib import django

#Descarga mi repositorio donde se encuentra mi app
def descargar():
	run('sudo apt-get update')
	run('sudo apt-get install -y git')
	run('sudo git clone https://github.com/pedrogazquez/appBares.git')

#Instalacion con las dependencias necesarias para ejecutar la app
def instalar():
	run('cd appBares && make install')

#Actualizar repo de app
def actualizar():
	run('cd appBares&& sudo git pull')

#Realizar los tests de la app
def test():
	run('cd appBares && make test')

#Ejecucion de la app
def ejecutarapp():
	run('cd appBares && sudo python manage.py runserver 0.0.0.0:80')

#Instalacion de docker y descarga de la imagen
def pull_docker():
	run('sudo apt-get update')
	run('sudo apt-get install -y docker.io')
	run('sudo docker pull pedrogazquez/appBares')
	
#Arranca Docker
def run_docker():
	run('sudo docker run -i -t pedrogazquez/appBares /bin/bash')

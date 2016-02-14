# Despliegue remoto: Fabric

[![presentacionDrive](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/rsz_presentaciones-de-google_zpsy1appnb5.png)](https://drive.google.com/open?id=1DVSnMu__rG9KGR-q_V1Uhn9PiZZBFtWmHxzygyiZpU8)

[Fabric](http://www.fabfile.org/) es una librería y herramienta de línea de comandos de Python que usaremos con la finalidad de hacer más eficiente el uso de SSH para el despliegue de nuestra app. 
Lo primero que hacemos es instalar Fabric con:

```
sudo pip install fabric
```
![installfabric](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202016-02-08%20112258_zpsjcfyrsqh.png)

Después lo que hago es añadir un archivo [fabfile.py](https://github.com/pedrogazquez/appBares/blob/master/fabfile.py) en el que defino las funciones que se podrán llevar a cabo mediante la línea de comandos:

```
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
```

Con estas funciones hago distintas cosas como explica el comentario que precede a cada una de ellas, una vez definido este archivo podremos llevar a cabo cualquiera de estas funciones mediante la herramienta de línea de comandos de Fabric:

```
fab -p contraseña -H aplicacion.cloudapp.net funcionAejecutar
```

En mi caso por ejemplo si ejecuto el siguiente comando:

```
dab -p myPassword -H vagrant@baresquesada.cloudapp.net ejecutarapp
```

El resultado es el de la función ejecutarapp del fabfile.py:

![ejecutarappFabfile](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/fabricTarea_zpspefzebrf.png)

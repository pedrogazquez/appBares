Lo primero que he hecho para crear la imagen, es crear el fichero [Dockerfile](https://github.com/pedrogazquez/appBares/blob/master/Dockerfile) el cual contiene lo siguiente:
```
FROM ubuntu:latest

#Autor
MAINTAINER Pedro Gazquez Navarrete <pedrogazqueznavarrete@gmail.com>

#Actualizar Sistema Base
RUN sudo apt-get -y update

#Descargar app
RUN sudo apt-get install -y git
RUN git clone https://github.com/pedrogazquez/appBares.git

#Instalar python
RUN sudo apt-get install -y python-setuptools
RUN sudo apt-get -y build-dep python-imaging --fix-missing
RUN sudo apt-get -y install libffi-dev
RUN sudo apt-get -y install python-dev
RUN sudo apt-get -y install build-essential
RUN sudo apt-get -y install python-psycopg2
RUN sudo apt-get -y install libpq-dev
RUN sudo apt-get -y install python2.7
RUN sudo easy_install pip
RUN sudo easy_install Pillow
RUN sudo pip install --upgrade pip

#Instalar app
RUN make install
```
He tenido un problema con la criptografía de python y tras mucho buscar e indagar lo he solucionado instalando el paquete **libffi-dev**.

Luego me he registrado en la web de [hub.docker](https://hub.docker.com/) y he autorizado a la aplicación para que se conecte a GitHub para así conectar el repositorio de mi proyecto para crear la imagen:

![imgAutoriza](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202015-12-05%20135317_zpsjamrchxm.png)

[Aqui esta mi imagen de docker](https://hub.docker.com/r/pedrogazquez/proyecto-iv/) y en la siguiente captura muestro la construcción automática de esta creando un "Automated Build" sobre el repositorio de mi proyecto de GitHub:

![DockerHub](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202015-12-10%20133939_zpsxdwwnyfs.png)

## Entorno de pruebas Docker en local

Para realizar esto en [mi makefile](https://github.com/pedrogazquez/appBares/blob/master/Makefile) he añadido las ordenes necesarias para crear el entorno, estas se llevan a cabo mediante make docker, que contiene:

```
	sudo apt-get update
 	sudo apt-get install -y docker.io
 	sudo docker pull pedrogazquez/appBares
 	sudo docker run -t -i pedrogazquez/appBares /bin/bash
 	
```

En las siguientes capturas muestro como se lleva a cabo la ejecución de los dos últimos comandos y como se lleva a cabo la ejecución de la app desde el contenedor local de Docker:

![captu1](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202015-12-10%20143906_zpsyzjp3w8p.png)

![captu2](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202015-12-10%20143906_zpsyzjp3w8p.png)

En estas capturas la ejecución la he hecho mediante el comando python y la app pero también se puede llevar a cabo con make run.

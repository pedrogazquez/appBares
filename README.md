# appBares

Proyecto de realización de una aplicación de bares y sus correspondientes tapas de Quesada (Jaén). Este proyecto se realizará tanto para la asignatura DAI (realización de la aplicación y despliegue en Heroku) como para IV ( infraestructura virtual necesaria para la realización de esta aplicación). La aplicación se realizará con el Framework de Python Django.

[Enlace a repo de la app](https://github.com/pedrogazquez/appBares).

[![Heroku](https://www.herokucdn.com/deploy/button.png)](https://appbaresdf.herokuapp.com/rango/)

[![Build Status](https://travis-ci.org/pedrogazquez/appBares.svg?branch=master)](https://travis-ci.org/pedrogazquez/appBares)

[![Build Status](https://snap-ci.com/pedrogazquez/appBares/branch/master/build_image)](https://snap-ci.com/pedrogazquez/appBares/branch/master)

[![Azure](http://azuredeploy.net/deploybutton.png)](http://baresquesada.cloudapp.net/rango/) 

##Descripción##
Realización de la infraestructura virtual necesaria para la aplicación (integración continua, despliegue en un PaaS/SaaS, entorno de pruebas DOCKER y virtualización de la app).

##Explicación##
Mi aplicación se encarga de llevar una serie de bares y sus correspondientes tapas de un pueblo (Quesada). TMi app también tendrá registro de usuarios, login y logout. Los usuarios registrados tienen la posibilidad de añadir tanto nuevos bares como nuevas tapas. También cualquiera puede votar sus tapas favoritas y así subirlas en el ranking de las 5 mejores tapas. Llevo la contabilidad de visitas que recibe cada bar en su página de tapas donde también se indica la localización en google maps de cada uno, así como un apartado que proporciona un gráfico de visitas de cada bar. Por útlimo mi aplicación también tiene 4 botones para cambiar el tamaño de letra en cualquier menú.


# Integración Continua

Para realizar los tests de mi proyecto he usado la libreria de test TestCase de django. Son tests flexibles y muy usados en este lenguaje. Los tests que he realizado los he integrado dentro de las herramientas de construcción, incluyendo un objetivo make test en [mi makefile](https://github.com/pedrogazquez/appBares/blob/master/Makefile). Para configurar el sistema de integración continua de forma que lance los tests automáticamente he usado Travis-CI . [Más info](https://github.com/pedrogazquez/appBares/blob/master/documentacion/integracionContinua.md)

# Despliegue de mi aplicación en un PaaS/SaaS: Heroku

[![Heroku](https://www.herokucdn.com/deploy/button.png)](https://appbaresdf.herokuapp.com/rango/)

[![Build Status](https://snap-ci.com/pedrogazquez/appBares/branch/master/build_image)](https://snap-ci.com/pedrogazquez/appBares/branch/master)

Para subir la app a Heroku hay que definir un archivo [procfile](https://github.com/pedrogazquez/appBares/blob/master/Procfile) que junto a nuestro [requirements.txt](https://github.com/pedrogazquez/appBares/blob/master/requirements.txt) nos hará falta para subir la aplicación a Heroku, [la he llamado appbaresdf](https://appbaresdf.herokuapp.com/rango/). Para ello lo que he hecho ha sido, primero registrarme en heroku, después he clonado el repositorio de mi app. Lo proximo que hay que hacer es crear el heroku con las órdenes pertinentes. [Más info](https://github.com/pedrogazquez/appBares/blob/master/documentacion/despliegueHeroku.md)

# DOCKER: Entorno de pruebas.
Lo primero que he hecho para crear la imagen, es crear el fichero [Dockerfile](https://github.com/pedrogazquez/appBares/blob/master/Dockerfile), luego una registrado en hub.docker autorizamos para que se conecte a GitHub y conectar el repositorio. Este es mi script:

```
#!/bin/bash
git clone https://github.com/pedrogazquez/appBares.git
cd appBares/VAGRANT-baresquesada/
vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box
vagrant up --provider=azure
vagrant provision 
```

[Más info](https://github.com/pedrogazquez/appBares/blob/master/documentacion/entornoDocker.md)

# Despliegue en un IaaS: Azure

[![Azure](http://azuredeploy.net/deploybutton.png)](http://baresquesada.cloudapp.net/rango/) 

Para realizar el despliegue en un IaaS (Infrastructure as a Service) que en mi caso ha sido en Azure, podemos desplegar la aplicación automáticamente con el script [despliegueAzure.sh](https://github.com/pedrogazquez/appBares/blob/master/VAGRANT-baresquesada/despliegueAzure.sh) ejecutando **./despliegueAzure.sh** que contiene lo siguiente:

```
#!/bin/bash
git clone https://github.com/pedrogazquez/appBares.git
cd appBares/VAGRANT-baresquesada/
vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box
vagrant up --provider=azure
vagrant provision 
```
Lo que hace este script es clonar mi repositorio de GitHub y acceder a el, luego lleva a cabo el despligue con Vagrant usando mi [Vagrantfile](https://github.com/pedrogazquez/appBares/blob/master/VAGRANT-baresquesada/Vagrantfile). [Aquí mi aplicación desplegada](http://baresquesada.cloudapp.net/rango/).

[Más info](https://github.com/pedrogazquez/appBares/blob/master/documentacion/despliegueAzure.md)

## Despliegue remoto: Fabric

[Fabric](http://www.fabfile.org/) es una librería y herramienta de línea de comandos de Python que usaremos con la finalidad de hacer más eficiente el uso de SSH para el despliegue de nuestra app. Con esta librería lo que hacemos es añadir un archivo [fabfile.py](https://github.com/pedrogazquez/appBares/blob/master/fabfile.py) en el que definimos una o varias funciones y que ejecutamos cada una desde la herramienta de línea de comandos fab.

[Más info](https://github.com/pedrogazquez/appBares/blob/master/documentacion/despliegueRemotoFabric.md)

##Inscripción en el certamen de Proyectos Libres de la UGR 2015-2016##
Aquí adjunto la imagen de la inscripción realizada correctamente en el Certamen:

![Inscripción](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/InscripcionUGR_zpsgkjszv6h.png)

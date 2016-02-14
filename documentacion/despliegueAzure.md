# Despliegue en un IaaS: Azure

[![Azure](http://azuredeploy.net/deploybutton.png)](http://baresquesada.cloudapp.net/rango/) 

[![presentacionDrive](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/rsz_presentaciones-de-google_zpsy1appnb5.png)](https://drive.google.com/open?id=1DVSnMu__rG9KGR-q_V1Uhn9PiZZBFtWmHxzygyiZpU8)

Lo que he hecho para realizar esta tarea es configurar Vagrant que sirve para crear y configurar entornos de despligue virtual (máquinas virtuales) y Ansible que sirve para hacer el despliegue de la app y realizar las distintas tareas de configuración y ejecución de esta.

Lo primero que hecho ha sido descargar la imagen de Vagrant, he instalado la versión estable más reciente que es la de [Vagrant 1.8.1x86_64.deb](https://releases.hashicorp.com/vagrant/1.8.1/).

Luego he instalado el provisionador de azure para Vagrant. Para esto ejecutamos:

```
vagrant plugin install vagrant-azure
```
![fotopluginvagrant](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202016-02-07%20220453_zpsggqexnuv.png)

Después de esto nos logueamos en azure con azure login y hacemos **azure account doownload**  esto nos proporciona un enlace al que deberemos acceder para descargar nuestros credenciales y una vez descargados hacemos:
```
azure account import Azure-2-5-2016-credentials.publishsettings
```
Siendo Azure-2-5-2016-credentials.publishsettings el archivo que nos hemos descargado al ejecutar el comando azure account download.

Lo siguiente que hacemos es generar los certificados que se subirán a Azure para perminirnos realizar las conexiones con nuestra máquina:

```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout azurevagrant.key -out azurevagrant.key
chmod 600 azurevagrant.key
openssl x509 -inform pem -in azurevagrant.key -outform der -out azurevagrant.cer
```

Ahora subimos el fichero **azurevagrant.cer** a Azure en el apartado Management Certificates:
![managcert](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202016-02-05%20164823_zpskywjh3fa.png)

Para autenticar Azure desde Vagranfile creamos un archivo .pem y lo concatemos el .key:
```
openssl req -x509 -key ~/.ssh/id_rsa -nodes -days 365 -newkey rsa:2048 -out azurevagrant.pem
cat azurevagrant.key > azurevagrant.pem
```
Luego creamos el fichero [Vagranfile](https://github.com/pedrogazquez/appBares/blob/master/VAGRANT-baresquesada/Vagrantfile):
```
VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = 'azure'
  config.vm.network "public_network"
  config.vm.network "private_network",ip: "192.168.56.10", virtualbox__intnet: "vboxnet0"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.define "localhost" do |l|
    l.vm.hostname = "localhost"
  end

  config.vm.provider :azure do |azure|
    azure.mgmt_certificate = File.expand_path('/home/pgazquez/Escritorio/appdefinitiva/azurevagrant.pem')
    azure.mgmt_endpoint = 'https://management.core.windows.net'
    azure.subscription_id = '686945bb-88d5-4919-bd0d-d2e0aeb76c29'
    azure.vm_image = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_3-LTS-amd64-server-20151218-en-us-30GB'
    azure.vm_name = 'baresquesada'
    azure.vm_user = 'vagrant'
    azure.vm_password = 'Pedro#1992'
    azure.vm_location = 'Central US' 
    azure.ssh_port = '22'
    azure.tcp_endpoints = '80:80'
  end

  config.vm.provision "ansible" do |ansible|
    ansible.sudo = true
    ansible.playbook = "ansiblebares.yml"
    ansible.verbose = "v"
    ansible.host_key_checking = false 
  end
end
```
En este Vagranfile en el primer bloque indicamos la imagen de la caja, el id de subscripción de azure, el usario el password, el puerto SSH, etc. En el segundo bloque se definen las características que tendrá nuestra máquina y por último en el tercero indicar que provisione la máquina mediante ansible y el nombre del fichero yml (ansiblebares.yml en mi caso).
Ahora definimos la variable de entorno ANSIBLE_HOSTS:
```
export ANSIBLE_HOSTS=~/Escritorio/appdefinitiva/ansible_hosts
```
Ahora añadimos lo siguiente en el archivo [ansible_hosts](https://github.com/pedrogazquez/appBares/blob/master/VAGRANT-baresquesada/ansible_hosts):
```
[localhost]
192.168.56.10
```
Y definimos el archivo [ansiblebares.yml](https://github.com/pedrogazquez/appBares/blob/master/VAGRANT-baresquesada/ansiblebares.yml):
```
- hosts: azure
  sudo: yes
  remote_user: vagrant
  tasks:
  - name: Instalar paquetes 
    apt: name=python-setuptools state=present
    apt: name=build-essential state=present
    apt: name=python-dev state=present
    apt: name=git state=present
  - name: Descargar aplicacion de GitHub
    git: repo=https://github.com/pedrogazquez/appBares.git dest=appBares clone=yes force=yes
  - name: Permisos de ejecucion
    command: chmod -R +x appBares
  - name: Instalar requisitos
    command: sudo pip install -r appBares/requirements.txt
  - name: ejecutar
    command: nohup sudo python appBares/manage.py runserver 0.0.0.0:80
```

Este instala los paquetes necesarios para ejecutar nuestra app después de descargar el repo de esta.
Ahora descargamos la box de azure con el siguiente comando:
```
vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box

```
![dummybox](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202016-02-05%20165928_zps2kqtfjqy.png)

Y ahora podemos proceder a ejecutar provider para que cree la app con el siguiente comando:
```
vagrant up --provider=azure
vagrant provision (si la máquina ya está creada)
```
La diferencia es que con el primer comando se crea la máquina en Azure a la vez que se procede a su despliegue configuración y ejecución, mientras que el segundo comando es para cuando ya tenemos creada la máquina en Azure.

Para automatizar todas estas tareas he creado un script [despliegueAzure.sh](https://github.com/pedrogazquez/appBares/blob/master/VAGRANT-baresquesada/despliegueAzure.sh):

```
#!/bin/bash
git clone https://github.com/pedrogazquez/appBares.git
cd appBares/VAGRANT-baresquesada/
vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box
vagrant up --provider=azure
vagrant provision 
```
Para ejecutarlo simplemente hacemos ./despliegueAzure.sh.

Una vez que se realizan todas las tareas se queda ejecutándose la app:
![imagenvagrantprovider](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202016-02-07%20230451_zps7ahmhy7f.png)

Y se podrá acceder a la app desde el navegador:
![imagennavegadorapp](http://i1042.photobucket.com/albums/b422/Pedro_Gazquez_Navarrete/Captura%20de%20pantalla%20de%202016-02-07%20231852_zpse9c2gii4.png)
[Enlace a app baresquesada](http://baresquesada.cloudapp.net/rango/)

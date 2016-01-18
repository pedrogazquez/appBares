install:
	sudo apt-get update
	sudo apt-get install -y python-dev
	sudo apt-get install -y python-pip
	sudo pip install --upgrade pip
	sudo pip install -r requirements.txt

test:
	python manage.py test
	
run:
	gunicorn tango_with_django_project.wsgi --log-file -
	
docker: 
	sudo apt-get update
	sudo apt-get install -y docker.io
	sudo docker pull pedrogazquez/appBares
	sudo docker run -t -i pedrogazquez/appBares /bin/bash

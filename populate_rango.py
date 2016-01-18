import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page, Bar, Tapa


def populate():
	marisol_bar = add_bar('Marisol')

	add_Tapa(relb=marisol_bar, 
		nombre="Rejos", 
		url="http://tengolareceta.com/wp-content/uploads/2011/09/espeluznao-o-espeluznado.jpg")

	add_Tapa(relb=marisol_bar, 
		nombre="Migas", 
		url="http://www.cocinayaficiones.com/wp-content/uploads/2015/05/tapa-de-chistorra-y-migas-4.jpg")

	add_Tapa(relb=marisol_bar, 
		nombre="Queso", 
		url="http://www.sobrerestaurantes.es/wp-content/uploads/2011/03/Tapas.jpg")

	tirol_bar = add_bar("Tirol")

	add_Tapa(relb=tirol_bar, 
		nombre="Lomo", 
		url="http://indalotapas.com/wp-content/uploads/2012/10/tapa-lomo-con-tomate-798x532.jpg")

	add_Tapa(relb=tirol_bar, 
		nombre="Hamburguesa", 
		url="https://media-cdn.tripadvisor.com/media/photo-s/07/0b/a5/27/tapa-de-mini-hamburguesa.jpg")

	add_Tapa(relb=tirol_bar, 
		nombre="Pisto", 
		url="http://baresdeandalucia.com/wp-content/uploads/2011/09/Tapa-de-Pisto-Tabernero-en-el-Bar-Crisol.jpg")

	sopero_bar = add_bar("Sopero")

	add_Tapa(relb=sopero_bar, 
		nombre="Serranito", 
		url="http://estaticos.fimagenes.com/imagenesred/10235777.jpg")

	add_Tapa(relb=sopero_bar, 
		nombre="Patatas Bravas", 
		url="http://gaftrestaurantgroup.com/wp-root/wp-content/uploads/2015/05/bravas.jpg")

	# Print out what we have added to the user.
	for c in Bar.objects.all():
		for p in Tapa.objects.filter(bar=c):
			print "- {0} - {1}".format(str(c), str(p))

def add_Tapa(relb, nombre, url, views=0):
    p = Tapa.objects.get_or_create(bar=relb, nombre=nombre)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_bar(name):
    c = Bar.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
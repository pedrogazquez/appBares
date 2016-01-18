from django.test import TestCase
from rango.models import Tapa, Bar, UserProfile
from django.test import Client


# Create your tests here.

class BarTestCase(TestCase):
	def setUp(self):
		Bar.objects.create(name="Jardin", dire="Calle carretera de Huesa, Quesada")
		barJar = Bar.objects.get(name="Jardin")
		Tapa.objects.create(bar=barJar,nombre="Croquetas",url="https://www.google.es/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwi2kfCY57PKAhVmKXIKHe6ZCQMQjRwIBw&url=https%3A%2F%2Fwww.tripadvisor.es%2FLocationPhotoDirectLink-g776189-d1002388-i65024081-Antiguo_Meson_Isla_Tortuga-Gines_Province_of_Seville_Andalucia.html&psig=AFQjCNGrN4TSgZql9DjUuGlYmbSPVV4A-Q&ust=1453221784141365")
		self.client = Client()
		
	def test_bartapa_exist(self):

		nuevobar = Bar.objects.get(name="Jardin")
		nuevatapa = Tapa.objects.get(nombre="Croquetas")
		self.assertEqual(nuevobar.dire, 'Calle carretera de Huesa, Quesada')
		self.assertEqual(nuevatapa.bar,nuevobar)
	
	def test_listabares(self):
		response = self.client.get('/rango/listaBares/')
		self.assertEqual(response.status_code, 200)
	
	def test_grafi(self):
		response = self.client.get('/rango/grafico/')
		self.assertEqual(response.status_code, 200)
		
	def test_about(self):
		response = self.client.get('/rango/about/')
		self.assertEqual(response.status_code, 200)
		
	def test_index(self):
		response = self.client.get('/rango/')
		self.assertEqual(response.status_code, 200)
		
	def test_login(self):
		response = self.client.get('/rango/login/')
		self.assertEqual(response.status_code, 200)


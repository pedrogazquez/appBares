from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('', 
		url(r'^$', views.index, name='index'),
		url(r'^about/$', views.about, name='about'),
		url(r'^add_category/$', views.add_category, name='add_category'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^listaBares/$', views.listaBares, name='listaBares'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^profile/$', views.profile, name='profile'),
		url(r'^register/$', views.register, name='register'),
		url(r'^add_page/(?P<bar_name_slug>[\w\-]+)/$', views.add_page, name='add_page'),
		url(r'^grafico/$', views.grafico, name='grafico'),
		url(r'^meGusta/(?P<tapa_title>[\w\-]+)/$', views.meGusta, name='meGusta'),
		url(r'^bar/(?P<bar_name_slug>[\w\-]+)/$', views.bar, name='bar'),)  # New!
		
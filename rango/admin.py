from django.contrib import admin
from rango.models import Bar, Tapa, Category, Page

# Add in this class to customized the Admin Interface
class BarAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
	
admin.site.register(Bar,BarAdmin)
admin.site.register(Tapa)
admin.site.register(Category)
admin.site.register(Page)
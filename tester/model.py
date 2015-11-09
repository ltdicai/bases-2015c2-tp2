from mongoengine import *

def init(dbase=None):
	dbase = dbase or 'tp2'
	return connect(dbase)

class Articulos(Document):
	cod_barras = IntField(db_field="codBarras", required=True, unique=True)
	nombre = StringField(required=True)
	sector = StringField(required=True)
	cant_unidades_vendidas = IntField(default=0)

	meta = {'collection': "articulos"}

class Compra(EmbeddedDocument):
	cantidad = IntField(required=True)
	articulo = ReferenceField(Articulos, required=True)

class ArticulosClientes(EmbeddedDocument):
	total = IntField(default=0)
	lista = ListField(field=EmbeddedDocumentField(Compra), default=list)

class Clientes(Document):
	dni = IntField(required=True, unique=True)
	nombre = StringField(required=True)
	edad = IntField(required=True)
	articulos = EmbeddedDocumentField(ArticulosClientes, default=ArticulosClientes) 

	meta = {'collection': "clientes"}

class ClientesAtendidos(EmbeddedDocument):
	cliente = ReferenceField(Clientes, db_field="_id", required=True)
	fecha = DateTimeField(required=True)

class SectoresEmpleado(EmbeddedDocument):
	sector = StringField(required=True)
	tarea = StringField(required=True)

class Empleados(Document):
	nro_legajo = StringField(db_field="nroLegajo", required=True, unique=True)
	nombre = StringField(required=True)
	clientes_mayores = ListField(field=EmbeddedDocumentField(ClientesAtendidos), default=list)
	clientes_menores = ListField(field=EmbeddedDocumentField(ClientesAtendidos), default=list)
	sectores = ListField(field=EmbeddedDocumentField(SectoresEmpleado), default=list)

	meta = {'collection': "empleados"}

	
class Sectores(Document):
	cod_sector = StringField(db_field="codSector", required=True, unique=True)
	empleados = ListField(field=ReferenceField(Empleados), default=[])

	meta = {'collection': "sectores"}

__all__ = ['Sectores', 'Empleados', 'Clientes', 'Articulos', 'SectoresEmpleado', 'Compra', 'init']
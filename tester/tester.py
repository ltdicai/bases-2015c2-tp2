import datetime

from mongoengine import DoesNotExist, MultipleObjectsReturned 
from pymongo import MongoClient

from model import *

class ErrorConsistencia(Exception):
	pass

class ErrorFaltanParametros(Exception):
	pass

def insertar_articulo(**kwargs):
	nuevo = Articulos(**kwargs)
	try:
		Sectores.objects.get(cod_sector=nuevo.sector) 
	except DoesNotExist:
		raise ErrorConsistencia('No existe sector %s' % nuevo.sector)
	nuevo.save()

def insertar_sector(**kwargs):
	Sectores(**kwargs).save()

def insertar_cliente(**kwargs):
	Clientes(**kwargs).save()

def insertar_empleado(**kwargs):
	Empleados(**kwargs).save()
	
def agregar_empleado(empleado=None, sector=None, tarea="Empleado"):
	if empleado is None:
		raise ErrorFaltanParametros("Falta empleado")
	if sector is None:
		raise ErrorFaltanParametros("Falta sector")
	if tarea is None:
		raise ErrorFaltanParametros("Falta tarea")
	try:
		obj_empleado = Empleados.objects.get(nro_legajo=empleado)
	except DoesNotExist:
		raise ErrorConsistencia('No existe empleado %s' % empleado)
	try:
		obj_sector = Sectores.objects.get(cod_sector=sector)
	except DoesNotExist:
		raise ErrorConsistencia('No existe sector %s' % sector)
	nuevo_sector = SectoresEmpleado(sector=sector, tarea=tarea)
	if nuevo_sector not in obj_empleado.sectores:
		obj_empleado.sectores.append(nuevo_sector)
	if obj_empleado not in obj_sector.empleados:
		obj_sector.empleados.append(obj_empleado)
	obj_empleado.save()
	obj_sector.save()

def comprar(articulo=None, cliente=None, cantidad=1):
	if articulo is None:
		raise ErrorFaltanParametros("Falta articulo")
	if cliente is None:
		raise ErrorFaltanParametros("Falta cliente")
	try:
		obj_articulo = Articulos.objects.get(cod_barras=articulo)
	except DoesNotExist:
		raise ErrorConsistencia('No existe articulo %s' % articulo)
	try:
		obj_cliente = Clientes.objects.get(dni=cliente)
	except DoesNotExist:
		raise ErrorConsistencia('No existe cliente %s' % cliente)
	obj_cliente.articulos.lista.append(Compra(articulo=obj_articulo, cantidad=cantidad))
	obj_cliente.articulos.total += cantidad
	obj_articulo.cant_unidades_vendidas += cantidad
	obj_cliente.save()
	obj_articulo.save()

def atender(cliente=None, empleado=None):
	if cliente is None:
		raise ErrorFaltanParametros("Falta cliente")
	if empleado is None:
		raise ErrorFaltanParametros("Falta empleado")
	fecha = datetime.datetime.utcnow()
	try:
		obj_cliente = Clientes.objects.get(dni=cliente)
	except DoesNotExist:
		raise ErrorConsistencia("No existe cliente %s" % cliente)
	try:
		obj_empleado = Empleados.objects.get(nro_legajo=empleado)
	except DoesNotExist:
		raise ErrorConsistencia("No existe empleado %s" % empleado)
	nuevo_obj = ClientesAtendidos(cliente=obj_cliente, fecha=fecha)
	if obj_cliente.edad >= 18:
		obj_empleado.clientes_mayores.append(nuevo_obj)
	else:
		obj_empleado.clientes_menores.append(nuevo_obj)
	obj_empleado.save()

db = MongoClient(host="localhost").tp2_test


if __name__ == "__main__":
	init(dbase='tp2_test')
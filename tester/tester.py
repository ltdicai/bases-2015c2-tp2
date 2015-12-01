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

def remover_articulo(cod_barras):
	try:
		obj = Articulos.objects.get(cod_barras=cod_barras)
	except DoesNotExist:
		raise ErrorConsistencia("No existe artículo %s" % cod_barras)
	for cliente in Clientes.objects():
		cant = 0
		res = []
		for compra in cliente.articulos.lista:
			if compra.articulo == obj:
				cant += compra.cantidad
			else:
				res.append(compra)
		cliente.articulos.lista = res
		cliente.articulos.total -= cant
		cliente.save()
	obj.delete()

def insertar_sector(**kwargs):
	Sectores(**kwargs).save()

def remover_sector(cod_sector):
	try:
		obj = Sectores.objects.get(cod_sector=cod_sector)
	except DoesNotExist:
		raise ErrorConsistencia("No existe sector %s" % cod_sector)
	articulos_a_borrar = Articulos.objects(sector=cod_sector)
	for articulo in articulos_a_borrar:
		remover_articulo(articulo.cod_barras)
	for empleado in obj.empleados:
		item = None
		for sector_empleado in empleado.sectores:
			if sector_empleado.sector == cod_sector.decode("utf-8"):
				item = sector_empleado
				break
		if item:
			empleado.modify(pull__sectores=item)
	obj.delete()


def insertar_cliente(**kwargs):
	Clientes(**kwargs).save()

def remover_cliente(dni):
	try:
		obj = Clientes.objects.get(dni=dni)
	except DoesNotExist:
		raise ErrorConsistencia("No existe cliente %s" % dni)
	for compra in obj.articulos.lista:
		compra.articulo.modify(dec__cant_unidades_vendidas=compra.cantidad)

	obj.delete()

def insertar_empleado(**kwargs):
	Empleados(**kwargs).save()

def remover_empleado(nro_legajo):
	try:
		obj = Empleados.objects.get(nro_legajo=nro_legajo)
	except DoesNotExist:
		raise ErrorConsistencia("No existe empleado %s" % nro_legajo)
	for sector in obj.sectores:
		obj_sector = Sectores.objects.get(cod_sector=sector.sector)
		obj_sector.modify(pull__empleados=obj)
	obj.delete()
	
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

def deshacer_agregar_empleado(empleado=None, sector=None, tarea="Empleado"):
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
	item = None
	for sectores_empleado in obj_empleado.sectores:
		if sectores_empleado.sector == sector and sectores_empleado.tarea == tarea:
			item = sectores_empleado
	if item:
		obj_sector.modify(pull__empleados=obj_empleado)
		obj_empleado.modify(pull__sectores=item)

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

def deshacer_comprar(articulo=None, cliente=None, cantidad=1):
	"""Encuentra alguna compra de `articulo` de parte de `cliente` y la 
	deshace. Si no la encuentra, entonces no hace nada.
	"""
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
	item = None
	for compra in obj_cliente.articulos.lista:
		if compra.articulo == obj_articulo and compra.cantidad == cantidad:
			item = compra
			break
	if item:
		obj_cliente.modify(pull__articulos__lista=item, dec__articulos__total=cantidad)
		obj_articulo.modify(dec__cant_unidades_vendidas=cantidad)


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
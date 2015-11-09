from mongoengine import DoesNotExist, MultipleObjectsReturned 

from model import *

class ErrorConsistencia(Exception):
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
	
def agregar_empleado(empleado, sector, tarea):
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

def comprar(articulo, cliente, cantidad=1):
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


if __name__ == "__main__":
	init(dbase='tp2_test')
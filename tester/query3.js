print("Los sectores donde trabaja exactamente 3 empleados");

print('db.sectores.find({"empleados": {$size: 3}})');

res = db.sectores.find({"empleados": {$size: 3}});




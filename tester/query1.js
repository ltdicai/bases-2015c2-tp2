print("Los empleados que atendieron clientes mayores de edad");

print('db.empleados.find({"clientes_mayores": {$exists: true, $not: {$size: 0}}})');

res = db.empleados.find({"clientes_mayores": {$exists: true, $not: {$size: 0}}});

//print(res.pretty());
//printjson("pe");



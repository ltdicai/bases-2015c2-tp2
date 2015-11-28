print("El empleado que trabaja en más sectores");

print('var max = db.empleados.aggregate([{$group: {_id:null, max: {$max: {$size: "$sectores"}}}}]).next().max');
print('db.empleados.find({sectores: {$size: max}})');

var max = db.empleados.aggregate([{$group: {_id:null, max: {$max: {$size: "$sectores"}}}}]).next().max

res = db.empleados.find({sectores: {$size: max}});





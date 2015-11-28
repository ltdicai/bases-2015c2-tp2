print("Cantidad de compras realizadas por clientes de misma edad");

print('db.clientes.aggregate([{$project: {"art_total": "$articulos.total", "edad": 1}}, {$group: {_id: "$edad", total: { $sum: "$art_total"}}}])');

res = db.clientes.aggregate([{$project: {"art_total": "$articulos.total", "edad": 1}}, {$group: {_id: "$edad", total: { $sum: "$art_total"}}}]);
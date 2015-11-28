print("Los artículos más vendidos");

print('var max_cant_unidades_vendidas = (db.articulos.aggregate([{$group : {_id: null, max : {$max : "$cant_unidades_vendidas"}}}])).next().max');
print('db.articulos.find("cant_unidades_vendidas" : max_cant_unidades_vendidas)');

var max_cant_unidades_vendidas = (db.articulos.aggregate([{$group : {_id: null, max : {$max : "$cant_unidades_vendidas"}}}])).next().max

res = db.articulos.find({"cant_unidades_vendidas" : max_cant_unidades_vendidas});




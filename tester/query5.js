print("Ranking de los clientes con mayor cantidad de compras")

print('db.clientes.aggregate([{$sort : {"articulos.total" : -1} } ])');

res = db.clientes.aggregate([{$sort : {"articulos.total" : -1} } ]);
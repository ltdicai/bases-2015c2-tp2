function getRandomIntInclusive(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

conn = new Mongo();
db = conn.getDB("sharding_test");

var people = db.people;

print(sh.status());

// for(var idx = 0; idx < 20; ++idx){
// 	people.insert({
// 		"nombre": "Damián" + idx,
// 		"password": "BUENACLAVE",
// 		"codigo_postal": getRandomIntInclusive(1, 1000000),
// 		"genero": "Masculino",
// 		"edad": idx*20*idx % 99,
// 		"fecha_creacion": new Date()
// 	})
// }
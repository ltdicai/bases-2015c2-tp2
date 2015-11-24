function getRandomIntInclusive(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

function dameRandom(arreglo){
	return arreglo[getRandomIntInclusive(0, arreglo.length - 1)];
}

function reverse(s){
    return s.split("").reverse().join("");
}

// conn = new Mongo("localhost:10003");
// db = conn.getDB("sharding_test");

var people = db.people;

print(sh.status());

var names_m = ["Damián", "Raúl", "Leandro", "Alejandro", "Javier", "Iván", "Patricio", "Hernán", "Santiago", "Floral"]

var names_f = ["Jazmín", "Clara", "Marina", "Merlina", "Laura", "Lucía", "Yanet", "Antonella", "María", "Patricia"]

db.people.createIndex({codigo_postal: 1})

sh.shardCollection("sharding_test.people", {codigo_postal: 1})

for(var idx = 0; idx < 20000; ++idx){
	var moneda = getRandomIntInclusive(0, 1);
	if (moneda == 0){
		var genero = "Masculino";
		var lista = names_m;
	}
	else{
		var genero = "Femenino";
		var lista = names_f;
	}
	people.insert({
		"nombre": [dameRandom(lista), dameRandom(lista), dameRandom(lista)].join(" "),
		"password": reverse(dameRandom(lista)),
		"codigo_postal": getRandomIntInclusive(1, 1000000),
		"genero": genero,
		"edad": idx*20*idx % 99,
		"fecha_creacion": new Date()
	})
}

print(db.people.getShardDistribution());
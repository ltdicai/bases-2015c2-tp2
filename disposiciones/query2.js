print("Devolver la cantidad de disposiciones por cada tipo definido");

var m = function(){
	if (this.Tipo != ""){
		emit(this["Tipo"], 1);
	}
}
var r = function(key, values) {
	return Array.sum(values); 
}

printjson(db.disposiciones.mapReduce(m,r,{out: {inline: 1}}));

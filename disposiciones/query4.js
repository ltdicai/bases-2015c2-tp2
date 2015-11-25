print("Devolver la mayor cantidad de páginas utilizadas por cada tipo de disposición");

var m = function(){
	var pagina_inicial = this["PaginaInicial"],
		pagina_final = this["PaginaFinal"];
	emit(this["Tipo"], pagina_final - pagina_inicial)
}

var r = function(key, values){
	var max = 0;
	// Calculo del maximo
	for(var i = 0; i < values.length; ++i){
		if (values[i] > max){
			max = values[i];
		}
	}
	return max;
}

var res = db.disposiciones.mapReduce(m, r, {out: {inline: 1}})
printjson(res);
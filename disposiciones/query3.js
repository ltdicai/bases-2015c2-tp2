print("Devolver la fecha más citada para todos los informes. Descartar las fechas embebidas en descripción");

function convertDate(str){
	if(str == "") return null;
	if(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?$/.test(str)){
		return new Date(str.replace(/^00/, "20"));
	}
	else if(/^\d{2}[-\/]\d{2}[-\/]\d{4}$/.test(str)){
		var parts = str.split(/[-\/]/);
		var aux = parts[0];
		parts[0] = parts[2];
		parts[2] = aux;
		return new Date(parts.join("-"));
	}
	else{
		return null;
	}
}

var m = function(){
	var fecha_boja = convertDate(this.FechaBOJA);
	var fecha_disp = convertDate(this.FechaDisposicion);
	if (fecha_boja){
		emit(fecha_boja, 1);
	}
	if(fecha_disp){
		emit(fecha_disp, 1);
	}
}
var r = function(key, values) {
	return Array.sum(values); 
}


var res = db.disposiciones.mapReduce(m,r,{out: {inline: 1}, scope: {convertDate: convertDate}})
printjson(res);

//Find max values
var max = null;
var res2 = [];
for(var idx = 0; idx < res.results.length; ++idx){
	var item = res.results[idx];
	if(max){
		if (max.value == item.value){
			res2.push(item);
		}
		else if (Math.max(max.value, item.value) != max.value) {
			res2 = [item];
			max = item;
		}
	}
	else{
		max = item;
		res2 = [item];
	}
}

printjson(res2);

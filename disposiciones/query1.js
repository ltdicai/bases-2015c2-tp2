print("Devolver la cantidad de disposiciones tipo resoluciones que se hayan realizado en Abril del 2013");

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
	var date = convertDate(this.FechaDisposicion);
	if(date){
		var month = date.getMonth(); 
		if (month == 3 && this.Tipo == "Resoluciones"){ 
			emit(this.Tipo, 1); 
		}
	}
}

var r = function(key,values) {
		return Array.sum(values)
	}

printjson(db.disposiciones.mapReduce(m,r,{out: {inline: 1}, scope: {convertDate: convertDate}}));

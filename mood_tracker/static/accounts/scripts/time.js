function today(datestring){
	var now = new Date();
	return (now.getDate() > datestring);
}

function get_cell(){
	var now = new Date();
	var x = now.getDate()
	return ".day_" + x;
}

function get_month(){
	var now = new Date();
	return now.getMonth() + 1;
}

function get_year(){
	var now = new Date();
	return now.getYear();
}
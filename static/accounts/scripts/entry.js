function time_of_day(which){

	$("#tod_dropdown").html(which);
	switch(which){
		case "Morning":
			$("#id_tod").val("M");
			break;
		case "Afternoon":
			$("#id_tod").val("A");
			break;
		case "Evening":
			$("#id_tod").val("E");
			break;
		case "Night":
			$("#id_tod").val("N");
			break;
	}
};

function number_to_symbol(){
	$('.latest').each(function() {
    	switch($(this).html().toString()){
    		case '-4':
    			$(this).html("----");
    			break;
    		case '-3':
    			$(this).html("---");
    			break;
    		case '-2':
    			$(this).html("--");
    			break;
    		case '-1':
    			$(this).html("-");
    			break;
    		case '0':
    			$(this).html("Normal");
    			break;
    		case '1':
    			$(this).html("+");
    			break;
    		case '2':
    			$(this).html("++");
    			break;
    		case '3':
    			$(this).html("+++");
    			break;
    		case '4':
    			$(this).html("++++");
    			break;
    	}
	});
};
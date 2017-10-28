$(document).ready(function(){
	$('.header-command-list').click(function() {
	  $(".command-list").slideToggle();
	  	if($(".text-header-command-list").html() == "Показать допустимые команды"){
				$(".text-header-command-list").html("Скрыть допустимые команды");
	  	} else {
				$(".text-header-command-list").html("Показать допустимые команды");
	  	}
	});

	$('#gm-example').click(function() {
		$('#command-line').val("minimize 0.5*x1**2 + 0.5*x2**2 - x1 - 2*x2 + 5 in 2*x1 + 3*x2 >= 6 and x1 + 4*x2 >= 5 and x1 >= 0 and x2 >= 0 from x1 = -4 to 4 and x2 = -4 to 4 use genetic hybrid {individuals_number: 5, generations_number: 10, survivors_number: 5}")
	});
});
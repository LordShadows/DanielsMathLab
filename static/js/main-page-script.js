$(document).ready(function(){
	$('.header-command-list').click(function() {
	  $(".command-list").slideToggle();
	  	if($(".text-header-command-list").html() == "Показать допустимые команды"){
				$(".text-header-command-list").html("Скрыть допустимые команды");
	  	} else {
				$(".text-header-command-list").html("Показать допустимые команды");
	  	}
	});
});
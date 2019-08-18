// Javascript file
// Project: Snarl
// Authro: hash3liZer

$(document).ready(function(){
	$(".left-nav").on('click', function(){
		$( ".slide-container" ).slideToggle( "fast" )
	})
	$("#login-form").on('submit', function(){
		var tsend = { 
			"username": $("#username").val(), 
			"password": $("#password").val()
		}
		if((tsend[ "username" ]) && (tsend[ "password" ])){
			$.ajax('/login', {
				method: 'POST',
				contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
				data: tsend,
				success: function(resp, status, robj){
					console.log( "successuful" )
				},
				error: function(robj, status, error){
					console.log( "error occured" )
				}
			})
		}else{
			var errbox = $( ".error-box" )
			errbox.text( "Please Input Both Fields To Login. " )
			errbox.show()
		}
		return false	
	})
})
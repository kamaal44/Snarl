// Javascript file
// Project: Snarl
// Author: hash3liZer

class Rrefresher{
	contructor(success){
		this.success = success
	}

	update(json, status, resp){
		return
	}

	refresh(){
		if(this.success){
			$.ajax("/current-status", {
				method: 'GET',
				success: this.update,
				error: function(resp, status, error){
					console.log( error )
				}
			})
		}
	}
}

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
			$.ajax('/login/', {
				method: 'POST',
				contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
				data: tsend,
				success: function(resp, status, robj){
					if((robj.status == 200) && (resp == "OK")){
						location.href = "/dashboard"
					}else{
						var errbox = $( ".error-box" )
						errbox.text( resp )
						errbox.show()
					}
				},
				error: function(robj, status, error){
					var errbox = $( ".error-box" )
					errbox.text( "An Unknown Error Has Occured. Please Refer to the Guide. " )
					errbox.show()
				}
			})
		}else{
			var errbox = $( ".error-box" )
			errbox.text( "Please Input Both Fields To Login. " )
			errbox.show()
		}
		return false	
	})
	$(".add, .recon").on('click', function(){
		var domname = $(".exe-container > input").val()
		if(domname){
			var action = $(this).attr( "class" )
			$.ajax("/executioner", {
				method: 'GET',
				contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
				data: {'action': action, 'domain': domname},
				success: function(json, status, response){
					if(response.status == 200){
						var obj = JSON.parse( json )
						if(obj.hasOwnProperty( "success" )){
							var refresher = new Rrefresher( obj[ "success" ] )
							refresher.refresh()
						}else{
							console.log( obj[ "error" ] )
						}
					}else{
						console.log( "Invalid Code Received. " )
					}
				},
				error: function(response, status, error){
					console.log( error )
				}
			})
			return false
		}else{
			alert( "Please entry a domain name" )
		}
	})
})
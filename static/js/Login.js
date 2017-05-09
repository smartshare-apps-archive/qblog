var btn_login;

var login_info = {
	"username":"",
	"password":""
}

var user_data = null;

var redirect_url = '/view_posts';


$(document).ready(function(){
	bindElements();
	bindEvents();
});

function bindElements(){
	btn_login = $("#btn_login");

	if(redirect_url == "/login" || redirect_url == '/login/'){
		redirect_url = '/'
	}


}

function bindEvents(){
	btn_login.click(submitLogin);
	
	$("#login_form").find("input").each(function(){
		$(this).change(updateGlobals);
	});

	$('#password').keypress(function (e) {
  		if (e.which == 13) {
  		  updateGlobals(e);
  		  submitLogin();
   		  return false;    
  							}

	});
}


function validateLogin(){
	return true;
}


function submitLogin(event){
	if (validateLogin() == true) {
		login(login_info);
	}

}

function authenticate(data){
	user_data = data;

	if (user_data != "invalid"){
		console.log("Success: " + user_data["username"]);
		window.location.href = redirect_url;
	}
	else{
		console.log("Invalid login.");
	}
}


function updateGlobals(event){
	var field = $(event.target);
	var field_id = event.target.id;
	var newVal = field.val();

	login_info[field_id] = newVal;
}
$(document).ready(function(){
  checkLoginStatus();
	
  $(".app-apply").click(function(event){
		event.preventDefault();
    if(!checkLoginStatus()){
			userObject={};
			userObject["firstName"] = $("#inputFirstName").val();
			userObject["lastName"] = $("#inputLastName").val();
			userObject["emailId"] = $("#inputEmail").val();
			userObject["phone"] = $("#inputCellNumber").val();
			userObject["zipCode"] = $("#inputZipCode").val();
			userObject = localStorage.setItem("userObject", JSON.stringify(userObject))
		}
		window.location.href = "/next";	
  });
  
	$('#myTab a').on('click', function (e) {
  	$(this).tab('show')
	})

	$(".user-logout").click(function(){
  	logOutUser();
	});
  function logInUser(){
		if (checkLoginStatus()){
			$(".nav-dropdown").show();
    }
  }
  function logOutUser(){
		localStorage.removeItem("userObject");
		$(".nav-dropdown").hide();
	}
  function checkLoginStatus() {
    if (localStorage.getItem("userObject") === null) {
			$(".nav-dropdown").hide();
  		return false;
    }else{
			return true;
    }
  }

});


function savePost(event){
	postData["post_content"] = replaceAll(postData["post_content"], '\n', '<br />')

	$.ajax({
	  method: "POST",
	  url: "/savePost",
	  dataType: "json",
	  data: { postData: JSON.stringify(postData) },
	  traditional: true
	})
	  .done(function( msg ) {
		location.reload();
	  });
	 
}



function createPost(event){

	$.ajax({
	  method: "POST",
	  url: "/createPost",
	  dataType: "json",
	  data: { postData: JSON.stringify(postData) },
	  traditional: true
	})
	  .done(function( msg ) {
		location.reload();
	  });
	 
}
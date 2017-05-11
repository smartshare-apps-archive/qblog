var btn_createPost;

$(document).ready(function(){
	btn_createPost = $("#btn_createPost");
	btn_createPost.click(createPost);

});




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
	var postData = {};
	postData["post_title"] = $("#input_postTitle").val();
	postData["post_type"] = $("#select_postType").val();
	postData["timeline_icon"] = "fa-file-text-o";

	$.ajax({
	  method: "POST",
	  url: "/createPost",
	  dataType: "json",
	  data: { postData: JSON.stringify(postData) },
	  traditional: true
	})
	  .done(function( post_id ) {
		location.href = "/edit/" + String(post_id);	
	});
	 
}


function deletePost(event){

	$.ajax({
	  method: "POST",
	  url: "/deletePost",
	  dataType: "json",
	  data: { postData: JSON.stringify(postData) },
	  traditional: true
	})
	  .done(function(msg) {
		location.href = "/view_posts";
	});
	 
}




function saveDatabaseConfig(event){

	$.ajax({
	  method: "POST",
	  url: "/saveDatabaseConfig",
	  dataType: "json",
	  data: { databaseConfig: JSON.stringify(databaseConfig) },
	  traditional: true
	})
	  .done(function(msg) {
		location.href = "/settings";
	});
	 
}



function saveRedisConfig(event){

	$.ajax({
	  method: "POST",
	  url: "/saveRedisConfig",
	  dataType: "json",
	  data: { redisConfig: JSON.stringify(redisConfig) },
	  traditional: true
	})
	  .done(function(msg) {
		location.href = "/settings";
	});
	 
}



function bulkDeletePosts(event){
	$.ajax({
	  method: "POST",
	  url: "/bulkDeletePosts",
	  dataType: "json",
	  data: { selectedPostIDs: JSON.stringify(selectedPostIDs) },
	  traditional: true
	})
	  .done(function(msg) {
		location.href = "/view_posts";
	});
	
}
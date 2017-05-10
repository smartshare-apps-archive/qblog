var btn_createPost;

$(document).ready(function(){
	bindElements();
	bindEvents();



});


function bindElements(){
	btn_createPost = $("#btn_createPost");


}


function bindEvents(){
	btn_createPost.click(createPost);


}


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
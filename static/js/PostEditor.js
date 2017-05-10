var post_editor;
var postData = {};


// button handles 
var btn_savePost;

$(document).ready(function(){
	populatePostData();

	bindElements();
	bindEvents();

	
});


function bindElements(){
	btn_savePost = $("#btn_savePost");
	btn_deletePost = $("#btn_deletePost");

	post_editor = new SimpleMDE({ 
		element: $("#post_editor_textarea")[0],
		initialValue: postData["post_content"],
		indentWithTabs: true,
		
		renderingConfig: {
			singleLineBreaks: true,
			codeSyntaxHighlighting: true,
		},
	});



}


function bindEvents(){
	post_editor.codemirror.on("change", function(){
		postData["post_content"] = post_editor.value();
		
		console.log(postData["post_content"]);
	});

	$(".post-data-input").each(function(){
		$(this).change(function(){
			var fieldID = $(this).attr('data-fieldID');
			var fieldValue = $(this).val();
			postData[fieldID] = fieldValue;
			console.log(postData);
		});
		

	});

	postData["post_content"] = replaceAll(postData["post_content"], '\n', '<br />')

	btn_savePost.click(savePost);
	btn_deletePost.click(deletePost);
}


function populatePostData(){

	$(".post-data-value").each(function(){

		var fieldID = $(this).attr('data-fieldID');
		var fieldValue = $(this).val();
		console.log("Field value:" + fieldValue);
		if(fieldID == "post_content" && fieldValue != ""){
			fieldValue = replaceAll(fieldValue, "<br />", '\n');
		}


		postData[fieldID] = fieldValue;
	});

	console.log(postData);
}




function replaceAll(str, find, replace) {
  return str.replace(new RegExp(find, 'g'), replace);
}



var selectedPosts = {};
var selectedPostIDs;

var post_action_bar;
var n_posts_selected;
var btn_bulkDeletePosts;

$(document).ready(function(){
	bindElements();
	bindEvents();

});


function bindElements(){
	post_action_bar = $("#post_action_bar");
	select_all_posts = $("#select_all_posts");
	n_posts_selected = $("#n_posts_selected");

	btn_bulkDeletePosts = $("#btn_bulkDeletePosts");

}


function bindEvents(){
	$(".selectTableItem").each(function(){
		$(this).change(function(){
			var postID = $(this).attr('data-postID');
			var isSelected = $(this).prop("checked");

			if(postID in selectedPosts){
				delete selectedPosts[postID];
			}
			else{
				selectedPosts[postID] = true;
			}

			refreshActionBar();
		});
	});

	btn_bulkDeletePosts.click(bulkDeletePosts);
}


function refreshActionBar(){
	var nPostsSelected = Object.keys(selectedPosts).length;
	selectedPostIDs = [];

	if (nPostsSelected > 0){
		post_action_bar.css('display','block');

		for(post_id in selectedPosts){
			selectedPostIDs.push(post_id);
		}


		n_posts_selected.html(String(nPostsSelected) + " post" + ((nPostsSelected > 1)? "s" : "") +  " selected");

		select_all_posts.unbind();

		select_all_posts.change(function(){
			var selectAll = $(this).prop("checked");

			if(selectAll){
				selectedPosts = {}
				$(".selectTableItem").each(function(){
					var postID = $(this).attr('data-postID');
					$(this).prop("checked", true);
					selectedPosts[postID] = true;
					selectedPostIDs.push(postID);
				})

			}
			else{

				selectedPosts = {}
				selectedPostIDs = [];
				$(".selectTableItem").each(function(){
					$(this).prop("checked", false);
				
				})

			}
			//console.log(selectedPosts);
			//console.log(selectedPostIDs);
			refreshActionBar();
		});
	}

	else{
		post_action_bar.css('display','none');
	}
}
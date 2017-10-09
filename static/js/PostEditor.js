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

			if(fieldID == "post_published"){
				if($(this).prop("checked") == true){
					fieldValue = 1;
				}
				else{
					fieldValue = 0;
				}
			}
			
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


(function(w,d,s,g,js,fjs){
  g=w.gapi||(w.gapi={});g.analytics={q:[],ready:function(cb){this.q.push(cb)}};
  js=d.createElement(s);fjs=d.getElementsByTagName(s)[0];
  js.src='https://apis.google.com/js/platform.js';
  fjs.parentNode.insertBefore(js,fjs);js.onload=function(){g.load('analytics')};
}(window,document,'script'));

function compare(metric){
	gapi.analytics.ready(function() {

	  // Step 3: Authorize the user.

	  var CLIENT_ID = '450799825815-t80f23bptjkvsudh72tmn6b4siqa8k1v.apps.googleusercontent.com';

	    gapi.analytics.auth.authorize({
    container: 'auth-button',
    clientid: CLIENT_ID,
  });

  // Step 4: Create the view selector.

  var viewSelector = new gapi.analytics.ViewSelector({
    container: 'view-selector'
  });

  // Step 5: Create the timeline chart.

  var timeline = new gapi.analytics.googleCharts.DataChart({
    reportType: 'ga',
    query: {
      'dimensions': 'ga:date',
      'metrics': metric,
      'start-date': '30daysAgo',
      'end-date': 'yesterday',
    },
    chart: {
      type: 'LINE',
      container: 'timeline'
    }
  });

  // Step 6: Hook up the components to work together.

  gapi.analytics.auth.on('success', function(response) {
    viewSelector.execute();
  });

  viewSelector.on('change', function(ids) {
    var newIds = {
      query: {
        ids: ids
      }
    }
    timeline.set(newIds).execute();
  });
});
}


$(function() {
    $('#calculate').bind('click', function() {
        var optionSelected = $( ".selectMetric option:selected" ).text();
        var expected = $( "#expected" ).val();
        var start_date = $( "#start_date" ).val();
        var end_date = $( "#end_date" ).val();
      $.getJSON($SCRIPT_ROOT + "/_get_metric", {
        metric: optionSelected,
        expected: expected,
        start_date: start_date,
        end_date: end_date
      }, function(data) {
        var summary = 'You forgot to fill all fields';
        if (data.error == true) {
            summary = data.result
        }
        else if (Number(data.expected) > Number(data.result)) {
            summary = 'Expected value greater than Actual';
        }
        else if (Number(data.expected) < Number(data.result)) {
            summary = 'Expected value less than Actual';
        }
        else if (Number(data.expected) == Number(data.result)) {
            summary = 'Expected value is equal to the Actual';
        }
        $("#metricResult").text(summary);
      });
      return false;
    });
  });


// button handles
var btn_saveRedisConfig;
var btn_saveDatabaseConfig;


var redisConfig = {};
var databaseConfig = {};

$(document).ready(function(){

	bindElements();
	bindEvents();

});


function bindElements(){
	btn_saveRedisConfig = $("#btn_saveRedisConfig");
	btn_saveDatabaseConfig = $("#btn_saveDatabaseConfig");

	$(".editor_input_field").each(function(){
		var settingID = $(this).attr('data-settingID');

		var fieldID = $(this).attr('data-fieldID');
		var fieldValue = $(this).val();

		if (settingID == "redis"){
			redisConfig[fieldID] = fieldValue;

			$(this).change(function(){
				var fieldID = $(this).attr('data-fieldID');
				var fieldValue = $(this).val();
				redisConfig[fieldID] = fieldValue;
				console.log(redisConfig);
			});

		}
		else if(settingID == "database"){
			databaseConfig[fieldID] = fieldValue;

			$(this).change(function(){
				var fieldID = $(this).attr('data-fieldID');
				var fieldValue = $(this).val();
				databaseConfig[fieldID] = fieldValue;
			});

		}


	});

}


function bindEvents(){
	btn_saveRedisConfig.click(saveRedisConfig);
	btn_saveDatabaseConfig.click(saveDatabaseConfig);
}
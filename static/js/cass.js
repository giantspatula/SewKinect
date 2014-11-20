$(document).ready(function(){
	console.log("cass.js imported")
	$("#leggings").hover(changeLeggings, changeSewDude);
	$("#a-line-skirt").hover(changeSkirt, changeSewDude);
	$("#circle-skirt").hover(changeCircleSkirt, changeSewDude);
	$("#custom-submit").submit(handleSubmit);
	$("#select-size").val(fillSizeForm);
});

function fillSizeForm(evt){
	evt.preventDefault
	var size = $("#select-size").val()
}

function loop(){
	//conect to Flask route
	//if response, process response
	//update fields 
	//set interval 
}

function changeSewDude(evt){
	console.log("sew dude back to normal!")
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude.png");
}

function changeLeggings(evt){
	console.log("sew dude wearing leggings!")
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_leggings.png");
}

function changeSkirt(evt){
	console.log("sew dude wearing skirt!")
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_skirt.png");
}

function changeCircleSkirt(evt){
	console.log("sew dude wearing skirt!")
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_circle.png");
}

function handleSubmit(evt){
	evt.preventDefault();
	console.log("Submit button pressed!")
	var waist = $("#waist");
	waist = waist.val();
	var hip = $("#hip");
	hip = hip.val();

	displayPatterns(evt)
}

function displayPatterns(evt){
	console.log("Gonna show you some patterns");
	$("#patterns").show("slow");
}
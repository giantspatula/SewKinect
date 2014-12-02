$(document).ready(function(){
	console.log("cass.js imported")
	$("#patterns").hide();
	$("#leggings").hover(changeLeggings, changeSewDude);
	$("#a-line-skirt").hover(changeSkirt, changeSewDude);
	$("#circle-skirt").hover(changeCircleSkirt, changeSewDude);
	$("#custom-measurements").submit(handleSubmit);
	$("#select-size").change(fillSizeForm);
	$("#standard-form").submit(dropDownSubmit);
	$("#kinect-click").click(getKinect);
	$("#select-kinect").change(fillKinectForm);
	$("#kinect-form").submit(KinectSubmit);
	$("#leggings").hover(changeLeggings, changeSewDude);
	$("#a-line-skirt").hover(changeSkirt, changeSewDude);
	$("#circle-skirt").click(draftCircle);
	$("#leggings").click(draftLeggings);
	$("#a-line-skirt").click(draftSkirt);
	$(".thigh-hover").hover(changeThigh, changeSewDude);
	$(".hip-hover").hover(changeHip, changeSewDude);
	$(".waist-hover").hover(changeWaist, changeSewDude);
	$(".waist-to-floor-hover").hover(changeWTF, changeSewDude);
	$(".waist-to-knee-hover").hover(changeWTK, changeSewDude);
	$(".waist-to-hip-hover").hover(changeWTH, changeSewDude);
});

function changeWTF(evt){
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_waist_to_floor.png");
}

function changeWTK(evt){
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_waist_to_knee.png");
}

function changeWTH(evt){
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_waist_to_hip.png");
}

function changeWaist(evt){
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_waist.png");
}

function changeThigh(evt){
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_thigh.png");
}

function changeHip(evt){
	console.log("hip hover!")
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_hip.png");
}


function draftCircle(evt){
	evt.preventDefault();
	$.get("/patterns/1", function(response){
		window.open(response)
	})
};

function draftSkirt(evt){
	evt.preventDefault();
	console.log("drafting skirt")
	$.get("/patterns/2", function(response){
		window.open(response)
	})
};

function draftLeggings(evt){
	evt.preventDefault();
	$.get("/patterns/3", function(response){
		window.open(response)
	})
};

function dropDownSubmit(evt){
	console.log("Dropdown submitted!");
	evt.preventDefault();
	console.log($("#select-size").val())
	if ($("#select-size").val() !== "0") {
		displayPatterns();
	}
};

function KinectSubmit(evt){
	evt.preventDefault();
	console.log($("#select-kinect").val())
	if($("#select-kinect").val().replace(/\"/g, "") !== "default"){
		console.log("Submitting!")
		var myVal = $("#select-kinect").val().replace(/\"/g, "").replace(/\u00a0/g, " ")
		var JSON = {"kinect": myVal}
		$.post("/custom", JSON, function(response){
			console.log(response)
			console.log(JSON)
		})
		displayPatterns(evt);
	}
}

function fillKinectForm(evt){
	evt.preventDefault;
	console.log("Filling Kinect form!")
	var myVal = $("#select-kinect").val().replace(/\"/g, "").replace(/\u00a0/g, " ")
	if (myVal !== "default"){
		$.get("/kinect", function(response){
			var obj = JSON.parse(response)[myVal]
			$("#kinect-waist").html(obj.waist.toFixed(2))
			$("#kinect-hip").html(obj.hip.toFixed(2))
			$("#kinect-thigh").html(obj.thigh.toFixed(2))
			$("#kinect-waist-to-hip").html(obj.waistToHip.toFixed(2))
			$("#kinect-waist-to-knee").html(obj.waistToKnee.toFixed(2))
			$("#kinect-waist-to-floor").html(obj.waistToFloor.toFixed(2))
		})
	}else{
			$("#kinect-waist").empty()
			$("#kinect-hip").empty()
			$("#kinect-thigh").empty()
			$("#kinect-waist-to-hip").empty()
			$("#kinect-waist-to-knee").empty()
			$("#kinect-waist-to-floor").empty()
	}
};

function getKinect(evt){
	evt.preventDefault;
	console.log("clicked Kinect")
	$("#kinect-waist").empty()
	$("#kinect-hip").empty()
	$("#kinect-thigh").empty()
	$("#kinect-waist-to-hip").empty()
	$("#kinect-waist-to-knee").empty()
	$("#kinect-waist-to-floor").empty()
	$.get("/kinect", function(response){
		console.log(response);
		$("#select-kinect").empty()
		$("#select-kinect").html("<option value=&quot;default&quot;></option>")
		$.each(JSON.parse(response), function(key, value){
			var format_key = key.replace(/ /g, '&nbsp;')
			new_html = "<option value=&quot;" + format_key + "&quot;>" + format_key +"</option>"
			$("#select-kinect").append(new_html)
		})
	})
};

function fillSizeForm(evt){
	console.log("Filling form!");
	evt.preventDefault;
	var route = "/JSON/" + $("#select-size").val();
	$.get(route, function(response){
		console.log(response)
		var obj = JSON.parse(response);
		console.log(obj)
		$("#standard-waist").html(obj.waist)
		$("#standard-hip").html(obj.hip)
		$("#standard-thigh").html(obj.thigh)
		$("#standard-waist-to-hip").html(obj.waistToHip)
		$("#standard-waist-to-knee").html(obj.waistToKnee)
		$("#standard-waist-to-floor").html(obj.waistToFloor)
	})
};

function changeSewDude(evt){
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude.png");
}

function changeLeggings(evt){
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_leggings.png");
}

function changeSkirt(evt){
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_skirt.png");
}

function changeCircleSkirt(evt){
	evt.preventDefault();
	$("#sewDude").attr("src", "static/img/sew_dude_circle.png");
}

function handleSubmit(evt){
	evt.preventDefault();
	console.log("Submit button pressed!");
	var JSON = {"custom":42,
"waist":$("#waist").val(),
"hip":$("#hip").val(),
"thigh":$("#thigh").val(),
"waistToHip":$("#waist-to-hip").val(),
"waistToKnee":$("#waist-to-knee").val(),
"waistToFloor":$("#waist-to-floor").val(),
"girth":8
};
	console.log(JSON);
	$.post("/custom", JSON, function(response){
		console.log(response)
		console.log(JSON)
	});
	displayPatterns(evt);
}

function displayPatterns(evt){
	console.log("Gonna show you some patterns");
	$("#patterns").show("slow");
}
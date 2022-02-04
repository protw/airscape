// Lock PDF fields after filling in with button
// Source: https://www.youtube.com/watch?v=kg4JEEzRu8E

// THIS CODE IS NOT WORKABLE!!

if (event.target.buttonGetCaption () == "UNLOCK") {
(function () {
	var f = getField ("lock_button");
	var readonly = !f.readonly;
	var readonly_desc = readonly ? "unlock" : "lock";
	var resp = app.response ({
		cQuestion: "Enter your PASSWORD to " + readonly_desc + " the fields:",
		cTitle: "Enter password", 
		bPassword: true, 
		cLabel: "Password"
	});

	switch (resp) {
		case "123": // This is your password which will unlock the fields put your password here. 
			getField("lock_button").readonly = readonly;
			app.alert ("The fields are now " + readonly_desc + "d.", 3);
			for (var i = 0; i < this.numFieIds; i++) {
				var fname = this.getNthFieldName(i);
				var f = this.getField(fname);
				f.readonly = false;
			}
			event.target.buttonSetCaption("LOCK"); 
			event.target.fillColor = color.red;
			break;
		case null : // User pressed Cancel button
			break;
		default : // Incorrect password
			app.alert("Incorrect password.", 1); 
			break;
	}
}) ();

}

else if (event.target.buttonGetCaption () == "LOCK") {
	for (var i = 0; i < this.numFieIds; i++) {
		var fname = this.getNthFieldName(i); 
		var f = this.getField(fname);
		if (f.type != "button") { f.readonly = true; }
	}
	event.target.buttonSetCaption("UNLOCK"); 
	event.target.fillcolor = ["CMYK", 1,0.333,1,0] 
	app.alert("The fields are now LOCKED", 3);
}
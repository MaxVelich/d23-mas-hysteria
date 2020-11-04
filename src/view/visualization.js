/*
This file contains some rendering specifics for the canvas and most draw functions for the individual parts of the simulation. We adjusted the code taken from the source below to our needs.

Source: https://github.com/projectmesa/mesa-examples/blob/master/examples/Flockers/flockers/simple_continuous_canvas.js
*/

var ContinuousVisualization = function(height, width, context) {
	var height = height;
	var width = width;
	var context = context;

	this.draw = function(objects) {
		for (var i in objects) {
			var p = objects[i];
			if (p.Shape == "rect")
				this.drawRectange(p.x, p.y, p.w, p.h, p.Color, p.Filled, p.text);
			if (p.Shape == "circle")
				this.drawCircle(p.x, p.y, p.r, p.Color, p.Filled, p.text, p.border, p.border_color);
		};
		this.drawCircle(50, 50, 2000, '#FF0000', true, '');
	};

	this.drawCircle = function(x, y, radius, color, fill, text, border, border_color) {
		var cx = x * width;
		var cy = y * height;
		var r = radius;

		context.beginPath();
		context.arc(cx, cy, r, 0, Math.PI * 2, false);
		context.closePath();

		if (fill) {
			context.fillStyle = color;
			context.fill();
		}


		// Add representation for theory of mind agent and for hazard
		if (border > 0){
            context.lineWidth = border ;
            context.strokeStyle = border_color;
            context.stroke();
            context.fillStyle = color;
            context.fill();
       }

	};

	this.drawRectange = function(x, y, w, h, color, fill, text) {
		context.beginPath();
		var dx = w * width;
		var dy = h * height;

		// Keep the drawing centered:
		var x0 = (x*width) - 0.5*dx;
		var y0 = (y*height) - 0.5*dy;

		context.strokeStyle = color;
		context.fillStyle = color;
		if (fill)
			context.fillRect(x0, y0, dx, dy);
		else
			context.strokeRect(x0, y0, dx, dy);
	};

	this.resetCanvas = function() {
		context.clearRect(0, 0, height, width);
		context.beginPath();
	};
};

var Simple_Continuous_Module = function(canvas_width, canvas_height, canvas_tag, legend_tag) {

	// Append it to body:
	var div = $(canvas_tag)[0];
	var div_legend = $(legend_tag)[0];
	$("body").append(div);
	$("body").append(div_legend);
	var canvas = $(canvas_id)[0];
	
	// Create the context and the drawing controller:
	var context = canvas.getContext("2d");
	var canvasDraw = new ContinuousVisualization(canvas_width, canvas_height, context);

	this.render = function(data) {
		canvasDraw.resetCanvas();
		canvasDraw.draw(data);
	};

	this.reset = function() {
		canvasDraw.resetCanvas();
	};

};
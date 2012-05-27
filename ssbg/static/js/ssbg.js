var ssbg = function() {
	$(".post img").replaceWith(function() {
		var src = $(this).attr("src");
		return '<a href="'+ src +'"><img src="'+ src +'" /></a>'
	});
}();

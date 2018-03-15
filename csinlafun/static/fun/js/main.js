

$(function($) {
	$all_as = $('.side-nav a');
	$side_nav_as = $('.side-nav>li>a');
	$side_nav_contents = $('.side-nav-content');
	$side_nav_as.click(function(e) {
		e.preventDefault();
		// remove all link active class, include children
		$all_as.removeClass('active');
		$(this).addClass('active');
		var i = $side_nav_as.index($(this));
		$side_nav_contents.removeClass('active').eq(i).addClass('active');
		$(this).closest('li').find('.sub-side-nav li:first-child a').click();
	});

	var $sub_side_nav_as = $('.sub-side-nav a');
	// next line is not flexible
	var $sub_side_nav_contents = $('.sub-side-nav-content');
	$sub_side_nav_as.click(function(e) {
		e.preventDefault();
		// trigger click on parent
		if (!$(this).closest('.has-sub').children('a').hasClass('active')) {
			$(this).closest('.has-sub').children('a').click();
		}
		
		$sub_side_nav_as.removeClass('active');
		$(this).addClass('active');
		var i = $sub_side_nav_as.index($(this));
		$sub_side_nav_contents.removeClass('active').eq(i).addClass('active');
	
	})
});
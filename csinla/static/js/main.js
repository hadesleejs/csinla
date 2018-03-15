

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

     $(function(){
             var jq_hour_start_select = $('#hour_start_select');
             var jq_hour_end_select = $('#hour_end_select');
             var jq_hour_start_select1 = $('#hour_start_select1');
             var jq_hour_end_select1 = $('#hour_end_select1');
             var mjq_hour_start_select = $('#mhour_start_select');
             var mjq_hour_end_select = $('#mhour_end_select');
             var mjq_hour_start_select1 = $('#mhour_start_select1');
             var mjq_hour_end_select1 = $('#mhour_end_select1');
             var carage = $('#carage1');
             var carage2 = $('#carage2');
             var year_start = $('#year_start');
             var year_end = $('#year_end');
            
             //初始化
             jq_hour_start_select_init();
             jq_hour_end_select_init();
             jq_hour_start_select_init1();
             jq_hour_end_select_init1();
             mjq_hour_start_select_init();
             mjq_hour_end_select_init();
             mjq_hour_start_select_init1();
             mjq_hour_end_select_init1();
             carage_init();
             carage_init2();
             carage_init3();
             carage_init4();
             
            
                 //结束时间初始化
                 
                 function jq_hour_end_select_init(){
                     //jq_hour_end_select.empty();
                     //jq_hour_end_select.append($('<option value="" selected>请选择</option>'));
                     for(var i =1;i<61;i++ ){
                                 jq_hour_end_select.append($('<option value='+i+'>'+i+'分钟</option>'));
                     }
                 }
                 //开始时间初始化
                 function jq_hour_start_select_init(){
                     //jq_hour_start_select.empty();
                     //jq_hour_start_select.append($(''));
                     for(var i =0;i<24;i++ ){
                                 jq_hour_start_select.append($('<option value='+i+'>'+i+'时</option>'));
                     }
                 }
                  function jq_hour_end_select_init1(){
                    // jq_hour_end_select1.empty();
                    // jq_hour_end_select1.append($('<option value="" selected>请选择</option>'));
                     for(var i =1;i<61;i++ ){
                                 jq_hour_end_select1.append($('<option value='+i+'>'+i+'分钟</option>'));
                     }
                 }
                 //开始时间初始化
                 function jq_hour_start_select_init1(){
                     //jq_hour_start_select1.empty();
                     //jq_hour_start_select1.append($('<option value="" selected>请选择</option>'));
                     for(var i =0;i<24;i++ ){
                                 jq_hour_start_select1.append($('<option value='+i+'>'+i+'时</option>'));
                     }
                 }
                  function mjq_hour_end_select_init(){
                     //mjq_hour_end_select.empty();
                    // mjq_hour_end_select.append($('<option value="" selected>请选择</option>'));
                     for(var i =1;i<61;i++ ){
                                 mjq_hour_end_select.append($('<option value='+i+'>'+i+'分钟</option>'));
                     }
                 }
                 //开始时间初始化
                 function mjq_hour_start_select_init(){
                     //mjq_hour_start_select.empty();
                     //mjq_hour_start_select.append($('<option value="" selected>请选择</option>'));
                     for(var i =0;i<24;i++ ){
                                 mjq_hour_start_select.append($('<option value='+i+'>'+i+'时</option>'));
                     }
                 }
                  function mjq_hour_end_select_init1(){
                     //mjq_hour_end_select1.empty();
                     //mjq_hour_end_select1.append($('<option value="" selected>请选择</option>'));
                     for(var i =1;i<61;i++ ){
                                 mjq_hour_end_select1.append($('<option value='+i+'>'+i+'分钟</option>'));
                     }
                 }
                 //开始时间初始化
                 function mjq_hour_start_select_init1(){
                    // mjq_hour_start_select1.empty();
                    // mjq_hour_start_select1.append($('<option value="" selected>请选择</option>'));
                     for(var i =0;i<24;i++ ){
                                 mjq_hour_start_select1.append($('<option value='+i+'>'+i+'时</option>'));
                     }
                 }
                 function carage_init(){
                     //mjq_hour_end_select1.empty();
                     //mjq_hour_end_select1.append($('<option value="" selected>请选择</option>'));
                     for(var i =1993;i<2019;i++ ){
                                 carage.append($('<option value='+i+'>'+i+'年</option>'));
                     }
                 }
                  function carage_init3(){
                     //mjq_hour_end_select1.empty();
                     //mjq_hour_end_select1.append($('<option value="" selected>请选择</option>'));
                     for(var i =1993;i<2019;i++ ){
                                 year_start.append($('<option value='+i+'>'+i+'</option>'));
                     }
                 }
                 function carage_init4(){
                     //mjq_hour_end_select1.empty();
                     //mjq_hour_end_select1.append($('<option value="" selected>请选择</option>'));
                     for(var i =1993;i<2019;i++ ){
                                 year_end.append($('<option value='+i+'>'+i+'</option>'));
                     }
                 }
                  function carage_init2(){
                     //mjq_hour_end_select1.empty();
                     //mjq_hour_end_select1.append($('<option value="" selected>请选择</option>'));
                     for(var i =1993;i<2019;i++ ){
                                 carage2.append($('<option value='+i+'>'+i+'年</option>'));
                     }
                 }
         });
         

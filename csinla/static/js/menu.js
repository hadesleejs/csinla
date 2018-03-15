$(function($) {
     $('.carouseladv').carousel({
  interval: 4000
});
    $('.mobile-nav-btn').click(function(e) {
        e.preventDefault();
        $('.user').slideDown();
    });
    $('.remove-nav').click(function(e) {
        e.preventDefault();
        $('.user').slideUp();
    });
    $('.has-sub-item').click(function(e) {
        e.preventDefault();
        $(this).next('.home-nav-sub-item').slideToggle();
    });

});
$(".useruser").each(function(){
   if($(this).html().length>3){
    $(this).css('font-size','12px');
   }
})
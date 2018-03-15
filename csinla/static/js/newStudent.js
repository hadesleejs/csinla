 $(function($) {
        $('.mobile-nav-btn').click(function(e) {
            e.preventDefault();
            $('.user').slideDown();
        });
        $('.remove-nav').click(function(e) {
            e.preventDefault();
            $('.user').slideUp();
        });
        // $('.user').click(function(e) {
        //     e.preventDefault();
        //     $('.user').slideUp();
        // });
        $(".mobile-nav-btn").on("click", function(e){
    $(".user").show();

    $(document).one("click", function(){
       e.preventDefault();
       $('.user').slideUp();
    });

    e.stopPropagation();
});
$(".user").on("click", function(e){
    e.stopPropagation();
});


    });
  

    (function ($) {
    'use strict';
    $('.item').on("click", function () {
    $(this).prev().slideToggle(100);
    $('.cc').not($(this).prev()).slideUp('fast');
    $('.item').css('display','block');
    $(this).css('display','none');
    });
    }(jQuery));

      
    
      $(function () {
    // 解析表情
    var comments = $(".u-main-content .u-main-section .u-bar-content .list-group");
    var length = comments.children(".list-group-item").length;
    console.log(length);

    for (var j = 1; j < length - 1; j++) {
        var item = comments.children().eq(j).children(".u-comment-content").children(".u-comment-text");
        item.html(item.html()).parseEmotion();
    }
    parseEmotion = true;
});
$(function () {
    // 解析表情
    var comments = $(".u-reply .reply_message_li");
    var length = comments.children(".media").length;
    console.log(length);

    for (var j = 0; j < length; j++) {
        var item = comments.children().eq(j).children(".media-body").children(".u-second-level-reply");
        item.html(item.html()).parseEmotion();
    }
    parseEmotion = true;
});

$(".emotion").on("click", function (event) {
    if (!$('#sinaEmotion').is(':visible')) {
        $(this).sinaEmotion();
        event.stopPropagation();
    }
});
function stuedit(){
  $("#stuedit").show();
  $(".Airport").hide();
  $("#returnlast").show();
}
 $("#myscroll").click(function(){
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#road").offset().top},1000);
                });
 $("#USC_nowbtn").click(function(){
  $("#USC_now").slideUp();
  $("#USC_applyf").show();
    

  });
 $("#USC_return").click(function(){
  $("#USC_now").show();
  $("#USC_applyf").hide();
    

  });
 $("#UCLA_nowbtn").click(function(){
  $("#UCLA_now").slideUp();
  $("#UCLA_applyf").show();
    

  });
 $("#UCLA_return").click(function(){
  $("#UCLA_now").show();
  $("#UCLA_applyf").hide();
    

  });
  $("#UCSB_nowbtn").click(function(){
  $("#UCSB_now").slideUp();
  $("#UCSB_applyf").show();
    

  });
 $("#UCSB_return").click(function(){
  $("#UCSB_now").show();
  $("#UCSB_applyf").hide();
    

  });
 $("#UCI_nowbtn").click(function(){
  $("#UCI_now").slideUp();
  $("#UCI_applyf").show();
    

  });
 $("#UCI_return").click(function(){
  $("#UCI_now").show();
  $("#UCI_applyf").hide();
    

  });
 $("#mreturn").click(function(){
  $("#mindex").show();
    $("#m-form").hide();
    

  });
  $("#myscroll ").hover(function() {
            $("#newtalk").hide();
            $("#newtalk1").show();
        }, function() {
             $("#newtalk1").hide();
            $("#newtalk").show();
        });
  $("#newemailw").hover(function() {
            $("#newemail").hide();
            $("#newemail1").show();
        }, function() {
             $("#newemail1").hide();
            $("#newemail").show();
        });
  function mform(a){
    $("#belong").val(a);
    $("#mindex").slideUp();
    $("#m-form").show();
  }
  $("#tisi").click(function(){
    $("#pctisi").hide();
  })
  $("#publish").click(function(){
  var postsform=new FormData($("#postsform")[0]);
  $.ajax({
    cache:false,
    type:"POST",
    url:"/accounts/add_sub/",
    data:postsform,
    async:true,
    processData:false,
    contentType:false,
    success:function(data){
      // alert(data.msg);
       $("#pctisi").show();
    }
  });




   
  })
   
  if(screen.width>1766){
  $(".imgmore").each(function(){
  $(this).children(".img3").each(function(i){
    j=i*0.3+19;
    z=192-(i*5);
    x=3-i;
  $(this).css("right",""+j+"%");
  $(this).css("margin-top",-z);
  $(this).css("z-index",x);

   });
});
}
else if(screen.width<1134 && screen.width>928){
 $(".imgmore").each(function(){
  $(this).children(".img3").each(function(i){
    j=i*0.3+10;
    z=192-(i*5);
    x=3-i;
    $(this).css("right",""+j+"%");
    $(this).css("margin-top",-z);
    $(this).css("z-index",x);

   });
});
}
else if(screen.width<1275 && screen.width>1134){
 $(".imgmore").each(function(){
  $(this).children(".img3").each(function(i){
    j=i*0.3+13;
    z=192-(i*5);
    x=3-i;
    $(this).css("right",""+j+"%");
    $(this).css("margin-top",-z);
    $(this).css("z-index",x);

   });
});
}
else{
  $(".imgmore").each(function(){
  $(this).children(".img3").each(function(i){
    j=i*0.3+17;
    z=192-(i*5);
    x=3-i;
    $(this).css("right",""+j+"%");
    $(this).css("margin-top",-z);
    $(this).css("z-index",x);

   });
});
}

function stuedit(){
   $("#stuedit").show();
  $(".Airport").hide();
  $("#returnlast").show();
}
 $("#myscroll").click(function(){
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#road").offset().top},1000);
                });
 $("#nowbtn").click(function(){
  $("#now").slideUp();
  $("#applyf").show();
    

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
  $("#tisi").click(function(){
    $("#pctisi").hide();
  })
  $("#publish").click(function(){
    $("#pctisi").show();
  })
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

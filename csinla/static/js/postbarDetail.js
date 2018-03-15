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

/*
 * 展开、收起回复
 * */
  if ($(".replyButton").html() == "收起回复") {
        
        
        $(".replyButton").html("收起回复").css({
            "border": "2px solid #dfdfdf",
            "border-bottom": "10px solid white"
        });
        $(".replyButton").siblings(".u-reply").show();}
       
  else {
        $(".replyButton").html("回复").css({
            "border": 0
        });
        $(".replyButton").removeClass("borderButton");
        $(".replyButton").siblings(".u-reply").hide();
  }

$(".replyButton").on("click", function () {
    if ($(this).html() == "回复") {
        $(this).html("收起回复").css({
            "border": "2px solid #dfdfdf",
            "border-bottom": "10px solid white"
        });
        $(this).siblings(".u-reply").show();
    } else {
        $(this).html("回复").css({
            "border": 0
        });
        $(this).removeClass("borderButton");
        $(this).siblings(".u-reply").hide();
    }
});

/*
 * 点赞
 * */
$(".likeIt").on("click", function () {
    $(this).toggleClass('like');
});

/*
 * sinaEmotion
 * */
$(".emotion").on("click", function (event) {
    if (!$('#sinaEmotion').is(':visible')) {
        $(this).sinaEmotion();
        event.stopPropagation();
    }
});
/*
 * 展开评论、收起评论
 */
$(".toggleComment").on("click", function () {
    var comments = $(".u-main-content .u-main-section .list-group");
    var length = comments.children().length;

    for (var i = 1; i < length - 1; i++) {
        comments.children().eq(i).toggleClass("hide");
    }

    if ($(this).data("flag") == true) {
        $(this).data("flag", false);
        $(this).html("展开评论<i class='fa fa-angle-double-down'></i>");
    } else {
        $(this).data("flag", true);
        $(this).html("收起评论<i class='fa fa-angle-double-up'></i>");
    }
});

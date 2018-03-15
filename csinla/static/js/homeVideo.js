$(function () {
    var parseEmotion = false;

    var comments = $(".u-main-content .u-video-comment .list-group");
    var length = comments.children().length;
    if (parseEmotion == false) {
        for (var j = 1; j < length; j++) {
            var item = comments.children().eq(j).children(".u-comment-content").children(".u-comment-text");
            item.html(item.html()).parseEmotion();
        }
        parseEmotion = true;
    }
});

$("#likeBtn").on("click", function () {
    $(this).toggleClass("like");
});

$("#saveBtn").on("click", function () {
    $(this).toggleClass("save");
});

/*
 * sinaEmotion
 * */
$("#emotion").on("click", function (event) {
    if (!$('#sinaEmotion').is(':visible')) {
        $(this).sinaEmotion();
        event.stopPropagation();
    }
});

/*
 * 展开、收起回复
 * */
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

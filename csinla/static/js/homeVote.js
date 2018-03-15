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
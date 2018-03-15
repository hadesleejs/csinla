$(".closeBtn").on('click', function (e) {
    e.preventDefault();
    $(this).parent().siblings(".img-big-wrapper").children("img").css("display", "none");

    var rotateCountL = $(this).parent().siblings(".img-big-wrapper").attr("data-rotateCountLeft");
    var rotateCountR = $(this).parent().siblings(".img-big-wrapper").attr("data-rotateCountRight");
    if (rotateCountL == 0 && rotateCountR != 0) {
        for (var i = 0; i < rotateCountR; i++) {
            $(this).siblings(".rotateL").trigger("click");
        }
        $(this).parent().siblings(".img-big-wrapper").attr("data-rotateCountRight", 0);
    } else if (rotateCountR == 0 && rotateCountL != 0) {
        for (var i = 0; i < rotateCountL; i++) {
            $(this).siblings(".rotateR").trigger("click");
        }
        $(this).parent().siblings(".img-big-wrapper").attr("data-rotateCountLeft", 0);
    }


    $(this).parent().siblings(".img-big-wrapper").children(".to-prev").show();

    $(this).parent().parent(".gallery").toggleClass("hide");
    $(this).parent().parent(".gallery").siblings(".img-wrapper").show();
});

$(".img-big-wrapper > img").on("click", function () {
    $(this).parent().siblings(".u-panel").children(".closeBtn").trigger("click");
});

$(".img-wrapper>img").on("click", function () {
    var index = $(this).index();

    $(this).parent().siblings(".gallery").children(".img-big-wrapper").attr("data-rotateCountLeft", 0).attr("data-rotateCountRight", 0);

    currentImg = index;

    $(this).parent().siblings(".gallery").children(".img-big-wrapper").attr("data-currentImg", index);

    if (index == 0) {
        $(this).parent().siblings(".gallery").children(".img-big-wrapper").children(".to-prev").hide();
    }
    if (index == ($(this).parent().children().length - 1)) {
        $(this).parent().siblings(".gallery").children(".img-big-wrapper").children(".to-next").hide();
    }

    $(this).parent().hide();
    $(this).parent().siblings(".gallery").toggleClass("hide");
    $(this).parent().siblings(".gallery").children(".img-big-wrapper").children("img").eq(index).css("display", "inline");
});


$(".rotateL").on("click", function (e) {
    e.preventDefault();

    var bigWrapper = $(this).parent().siblings(".img-big-wrapper");
    var rotateCountL = parseInt(bigWrapper.attr("data-rotateCountLeft"));
    var rotateCountR = parseInt(bigWrapper.attr("data-rotateCountRight"));

    var dataCurrentImg = $(this).parent().siblings(".img-big-wrapper").attr("data-currentImg");

    if (rotateCountR == 0) {
        rotateCountL++;
    } else {
        rotateCountL = 4 - rotateCountR + 1;
        rotateCountR = 0;
    }

    var imgWidth = bigWrapper.children("img").eq(dataCurrentImg).width();
    var imgHeight = bigWrapper.children("img").eq(dataCurrentImg).height();

    if (rotateCountL % 2 != 0) {
        var temp = imgWidth;
        imgWidth = imgHeight;
        imgHeight = temp;
    }

    bigWrapper.css("height", imgHeight + "px");

    var degree = 90 * rotateCountL;
    var distance = (imgHeight - imgWidth) / 2;

    if (rotateCountL % 2 == 0) {
        bigWrapper.children("img").eq(dataCurrentImg).css({
            "transform": "rotate(-" + degree + "deg)"
        });
    } else if (rotateCountL == 1) {
        bigWrapper.children("img").eq(dataCurrentImg).css({
            "transform": "rotate(-" + degree + "deg) translate(-" + distance + "px, 0px)"
        });
    } else {
        bigWrapper.children("img").eq(dataCurrentImg).css({
            "transform": "rotate(-" + degree + "deg) translate(" + distance + "px, 0px)"
        });
    }

    if (rotateCountL == 4) {
        rotateCountL = 0;
    }

    bigWrapper.attr("data-rotateCountLeft", rotateCountL);
    bigWrapper.attr("data-rotateCountRight", rotateCountR);
});

$(".rotateR").on("click", function (e) {
    e.preventDefault();

    var bigWrapper = $(this).parent().siblings(".img-big-wrapper");
    var rotateCountL = parseInt(bigWrapper.attr("data-rotateCountLeft"));
    var rotateCountR = parseInt(bigWrapper.attr("data-rotateCountRight"));

    var dataCurrentImg = $(this).parent().siblings(".img-big-wrapper").attr("data-currentImg");

    if (rotateCountL == 0) {
        rotateCountR++;
    } else {
        rotateCountR = 4 - rotateCountL + 1;
        rotateCountL = 0;
    }

    var imgWidth = bigWrapper.children("img").eq(dataCurrentImg).width();
    var imgHeight = bigWrapper.children("img").eq(dataCurrentImg).height();

    if (rotateCountR % 2 != 0) {
        var temp = imgWidth;
        imgWidth = imgHeight;
        imgHeight = temp;
    }

    bigWrapper.css("height", imgHeight + "px");

    var degree = 90 * rotateCountR;
    var distance = (imgHeight - imgWidth) / 2;

    if (rotateCountR % 2 == 0) {
        bigWrapper.children("img").eq(dataCurrentImg).css({
            "transform": "rotate(" + degree + "deg)"
        });
    } else if (rotateCountR == 1) {
        bigWrapper.children("img").eq(dataCurrentImg).css({
            "transform": "rotate(" + degree + "deg) translate(" + distance + "px, 0px)"
        });
    } else {
        bigWrapper.children("img").eq(dataCurrentImg).css({
            "transform": "rotate(" + degree + "deg) translate(-" + distance + "px, 0px)"
        });
    }

    if (rotateCountR == 4) {
        rotateCountR = 0;
    }

    bigWrapper.attr("data-rotateCountLeft", rotateCountL);
    bigWrapper.attr("data-rotateCountRight", rotateCountR);
});

$(".to-prev").on("click", function () {
    var dataCurrentImg = $(this).parent().attr("data-currentImg");

    $(this).siblings("img").eq(dataCurrentImg).css({
        "transform": "rotate(0deg)"
    });
    $(this).parent().css("height", "auto");

    $(this).parent().children("img").eq(dataCurrentImg).css("display", "none");
    $(this).parent().css("height", "auto");
    dataCurrentImg -= 1;
    if (dataCurrentImg == 0) {
        $(this).hide();
    }
    $(this).parent().children("img").eq(dataCurrentImg).css("display", "block");

    $(this).parent().attr("data-currentImg", dataCurrentImg);

    if (dataCurrentImg != $(this).parent().children("img").length - 1) {
        $(".to-next").show();
    }
});

$(".to-next").on("click", function () {
    var bigWrapper = $(this).parent();

    var dataCurrentImg = parseInt($(this).parent().attr("data-currentImg"));

    $(this).siblings("img").eq(dataCurrentImg).css({
        "transform": "rotate(0deg)"
    });
    $(this).parent().css("height", "auto");

    bigWrapper.children("img").eq(dataCurrentImg).css("display", "none");

    bigWrapper.css("height", "auto");
    dataCurrentImg = dataCurrentImg + 1;

    if (dataCurrentImg == bigWrapper.children("img").length - 1) {
        $(this).hide();
    }

    bigWrapper.children("img").eq(dataCurrentImg).css("display", "block");

    bigWrapper.attr("data-currentImg", dataCurrentImg);

    if (dataCurrentImg != 0) {
        $(".to-prev").show();
    }
});
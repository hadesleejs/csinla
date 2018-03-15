    var player = videojs("home_video", {
        techOrder: ["html5", "flash"],
        controlBar: {
            captionsButton: false,
            subtitlesButton: false
        },
        poster: "images/home-video_bg.png"
    });
    window.addEventListener('popstate',function(){
            
            window.location.reload();

       })
    
    $('.a_contact').click(function(){
        if($(".Contactus").css('display')=="none"){
          $(".Contactus").show();
         // $(".footer").css("position","relative");
         event.preventDefault();
                    $("html,body").animate({scrollTop:$("#contactid").offset().top},1000)}
        else{
            $(".Contactus").css('display','none')
        }
    });
     
$(function () {
    $(".nav .life .box").on("mouseenter", function () {
        //$(this).toggleClass("flipped");
        $(this).children("div:eq(0)").css("display", "none");
        $(this).children("div:eq(1)").css("display", "block");
    }).on("mouseleave", function () {
        //$(this).toggleClass("flipped");
        $(this).children("div:eq(0)").css("display", "block");
        $(this).children("div:eq(1)").css("display", "none");
    });

    $(".nav .profession .box2").on("mouseenter", function () {
        //$(this).toggleClass("flipped");
        $(this).children(":first").css("display", "none");
        $(this).children(":last").css("display", "block");
    }).on("mouseleave", function () {
        //$(this).toggleClass("flipped");
        $(this).children(":first").css("display", "block");
        $(this).children(":last").css("display", "none");
    });

    $(".footer #votePanel a").on("mouseenter click", function () {
        event.preventDefault();
        $(".footer .voteBox").animate({height: "315px"}, 500);
        $(".footer .voteBox").css("z-index", 10);
        $(".footer .voteBox").on("mouseleave", function () {
            $(this).animate({height: "0"}, 500);
            $(this).css("z-index", 0);
        });
    });

    $(".footer #videoPanel a").on("mouseenter click", function () {
        event.preventDefault();
        $(".footer .videoBox").animate({height: "255px"}, 500);
        $(".footer .videoBox").on("mouseleave", function () {
            $(this).animate({height: "0"}, 500);
        });
    });
});
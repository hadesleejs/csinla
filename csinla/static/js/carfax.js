
$(".erwei").click(function(){
   $(".alert3").show();
   $(".imgma2").hide();
   $(".imgma").show();
});
$(".mberwei").click(function(){
   $(".alert3").show();
   $(".imgma").show();
   $(".imgma2").hide();
});
$(".alert3").click(function(){
   $(".alert3").hide();
});
$(".erwei2").click(function(){
   $(".alert3").show();
   $(".imgma").hide();
   $(".imgma2").show();
});
$(".mberwei2").click(function(){
   $(".alert3").show();
   $(".imgma").hide();
   $(".imgma2").show();

});

$(".img-responsive").click(function(){
  $(".alert").hide();
  $(".mb-alert").hide();
});
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
$(".sub").click(function(){
    var vin=$("#vin").val();
    var name=$("#name").val();
    var email=$("#email").val();
    var wechat=$("#weiixn").val();
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

 $.ajax({
                type: "POST",
                dataType: "json",
                url: "/accounts/carfax/",
                 traditional: true,
                data: {'vin':vin,'name':name,'email':email,'wechat':wechat,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 if(data.code==0){
                  $(".alert").show();
                   $(".vin").each(function(){
                    $(this).val("");
                  });
                }
                else if (data.code==2) {
                  window.location.href="/accounts/login/?next=/accounts/carfax/";
      
                }
                 else{
                  alert(data.msg);
                 }
               
         
  
                },
                error: function (err) {
                    alert("err:" + err);
                     //$(".alert").show();
                }
         });
});
$(".mb-sub").click(function(){
    var mbvin=$("#mb-vin").val();
    var mbname=$("#mb-name").val();
    var mbemail=$("#mb-email").val();
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    var mbwechat=$("#mb-weiixn").val();

 $.ajax({
                type: "POST",
                dataType: "json",
                url: "/accounts/carfax/",
                 traditional: true,
                data: {'vin':mbvin,'name':mbname,'email':mbemail,'wechat':mbwechat,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 
                 
                if(data.code==0){
                  $(".mb-alert").show();
                  $(".mb-vin").each(function(){
                      $(this).val("");
                    });
                }
                else if (data.code==2) {
                  window.location.href="/accounts/login/?next=/accounts/carfax/";
      
                }
                 else{
                  alert(data.msg);
                 }
               
         
  
                },
                error: function (err) {
                    alert("err:" + err);
                    //$(".mb-alert").show();
                }
         });
});
$("#scroll").click(function(){
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#chanpin").offset().top},1000);
                });
$("#scroll1").click(function(){
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#procedure").offset().top},1000);
                });
$("#scroll2").click(function(){
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#partner").offset().top},1000);
                });
$("#scroll3").click(function(){
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#connect").offset().top},1000);
                });
$("#mbscroll").click(function(){
    //e.preventDefault();
    $('.user').slideUp();
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#mbchanpin").offset().top},1000);
                });
$("#mbscroll1").click(function(){
    //e.preventDefault();
    $('.user').slideUp();
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#mbprocedure").offset().top},1000);
                });
$("#mbscroll2").click(function(){
    //e.preventDefault();
    $('.user').slideUp();
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#mbpartner").offset().top},1000);
                });
$("#mbscroll3").click(function(){
    //e.preventDefault();
    $('.user').slideUp();
    event.preventDefault();
    $("html,body").animate({scrollTop:$("#mbconnect").offset().top},1000);
                });
$(".alert-btn").click(function(){
      $(".alert").hide();
      $(".vin").each(function(){
        $(this).val("");
      });
});
$(".mb-alert-btn").click(function(){
      $(".mb-alert").hide();
      $(".mb-vin").each(function(){
        $(this).val("");
      });
});
$(".alert-btn1").click(function(){
    window.location.href="/";
      
});
$(".mb-alert-btn1").click(function(){
     window.location.href="/";
});
function login(){
                  window.location.href="/accounts/login/?next=/accounts/carfax/";

}

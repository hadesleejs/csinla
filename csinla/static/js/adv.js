$(document).scroll(function(){
    var aa=$(document).scrollTop();
    if(aa>388){
        $("#A3").css('position','fixed');
        $("#A3").css('width', '17.8%');
        // $("#A3").css('height', 'auto');
        $("#A3").css('top', '0');
        // $("#A3").css('margin-left', '-8.3%');
        $("#A5").css('position','fixed');
        $("#A5").css('width', '17.8%');
        // $("#A5").css('height', 'auto');
        // alert($("#A3 img").height());
        var b=$("#A3 img").height();
        $("#A5").css('top', ''+b+'px');
        // $("#A5").css('margin-left', '-8.3%');

    }
    else if(aa<388){
        $("#A3").css('position','');
        $("#A3").css('width', '100%');
        $("#A3").css('height', 'auto');
        $("#A3").css('top', '');
        $("#A3").css('margin-left', '');
        $("#A5").css('position','');
        $("#A5").css('width', '100%');
        $("#A5").css('height', 'auto');
        $("#A5").css('top', '');
        $("#A5").css('margin-left', '');
    }
    
});
function contact(a,read){

    // $('#c'+a)
    $('#c'+a).toggle();
    if(read==0){
        var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/posts/postmessage/leave/",
            data: {
                'operate':'collect_read',
                'pmid':a,
                'csrfmiddlewaretoken':csrfmiddlewaretoken
            },
            success: function (data) {
                if(data.code!=0){
                    alert(data.msg);
                }

            },
            error: function (err) {
                alert("err:" + err);
            }
        });

    }
  

}
function contact1(b,read){

    // $('#'+b)
    $('#cm'+b).toggle();
    if(read==0){
        var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/posts/postmessage/leave/",
            data: {
                'operate':'collect_read',
                'pmid':b,
                'csrfmiddlewaretoken':csrfmiddlewaretoken
            },
            success: function (data) {
                if(data.code!=0){
                    alert(data.msg);
                }

            },
            error: function (err) {
                alert("err:" + err);
            }
        });

    }
  

}

function reply_comment(o){

    $('#'+o)
        $('#'+o).toggle();
  

}
function reply_comment1(l){

    $('#'+l)
        $('#'+l).toggle();
  

}
$("#othercollect").click(function(){
 $.ajax({url:"../deletenotice/",async:false});
  
  });
function pli(p){
    var operate="reply";
    
    var post=$(".posts_id").val();
    var reply_message=p;
    var content=$("#intext"+p+"").val();
    //alert(content);
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    //alert(reply_message);
    $.ajax({
                type: "POST",
                dataType: "json",
                url: "/posts/postmessage/leave/",

                data: {'operate':operate,'post':post,'reply_message':reply_message,'content':content,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                

                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 alert(data.msg);
                 window.location.reload();
                
                
      
         
  
                },
                error: function (err) {
                    alert("err:" + err);
                }
            });

           
}
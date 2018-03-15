// var addres= document.getElementById("addres").innerText;
// document.getElementById('destination-input').value=addres;
jq('#demo1').banqh({
    box:"#demo1",//总框架
    pic:"#ban_pic1",//大图框架
    pnum:"#ban_num1",//小图框架
    prev_btn:"#prev_btn1",//小图左箭头
    next_btn:"#next_btn1",//小图右箭头
    pop_prev:"#prev2",//弹出框左箭头
    pop_next:"#next2",//弹出框右箭头
    prev:"#prev1",//大图左箭头
    next:"#next1",//大图右箭头
    pop_div:"#demo2",//弹出框框架
    pop_pic:"#ban_pic2",//弹出框图片框架
    pop_xx:".closeimg",//关闭弹出框按钮
    mhc:".mhc",//朦灰层
    autoplay:true,//是否自动播放
    interTime:5000,//图片自动切换间隔
    delayTime:400,//切换一张图片时间
    pop_delayTime:400,//弹出框切换一张图片时间
    order:0,//当前显示的图片（从0开始）
    picdire:true,//大图滚动方向（true为水平方向滚动）
    mindire:true,//小图滚动方向（true为水平方向滚动）
    min_picnum:5,//小图显示数量
    pop_up:true//大图是否有弹出框
})

var hash=window.location.hash.replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
if((window.location.href).indexOf("#")>-1){
    $("#m"+hash).parent('.u-reply').show();
    window.location.href="#m"+hash;

}
else{
     $("#m"+hash).parent('.u-reply').hide();
}

     var i=1;
    $('#books_list .item_index').each(function() {
        $this=$(this);
        $this.html('商品'+i);
        i=i+1;
        $(".goods_content td").css("padding","0px 5px")
    })
    
    if (i==2) {$(".goods_title").hide();$(".goods_content td").css("padding","0px 0px")}
    var j=1;
    $('#mbooks_list .item_index').each(function() {
        $this=$(this);
        $this.html('商品'+j);
        j=j+1;
    })
    if (j==2){$(".goods_title").hide();}



$(function(){

    var num=$('#slider').find('li').size();

    $('.bcount').text(num); 

    $('.b_btn').click(function(){

        $(this).toggleClass('b_btn_active');

        $('.intro').toggle();

    })

})

var tt=new TouchSlider({id:'slider','auto':'-1',fx:'ease-out',direction:'left',speed:600,timeout:5000,'before':function(index){

    var es=document.getElementById('slider').getElementsByTagName('li');

    var it=$(es[index]).index()+1;  

    $('.bi').text(it);  

    var tx=$(es[index]).find('p').text();   

    $('.title').text(tx);

}});
function re(i){
    // var rp=$(this).arr('id');
    // alert(rp);
    $(".reply_message_sign").val(i);
   //$("#intext").val("回复");
   // $(".ff textarea").addClass("intext"+i);
}
//回复
function pli(p){
    var operate="reply";
    
    var post=(window.location.pathname).replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
    var reply_message=$('#rep'+p).val();
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
//发表评论
$("#publish").click(function(){
    //alert($("#contenttxt").val());
    var operate="reply";
    var content=$("#contenttxt").val();
    var post=(window.location.pathname).replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    //alert(post);
    $.ajax({
                type: "POST",
                dataType: "json",
                url: "/posts/postmessage/leave/",

                data: {'operate':operate,'post':post,'content':content,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                

                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 alert(data.msg);
                
                window.location.reload()
      
         
  
                },
                error: function (err) {
                    alert("err:" + err);
                }
            });

           
});
//删除
function del(p){
    var operate="delete";
    
    var post=(window.location.pathname).replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
    // var reply_message=$('.reply_message_sign').val();
    // var pmid=$('#rep'+p).val();
    //var content=$("#intext"+p+"").val();
    //alert(content);
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    //alert(reply_message);
    $.ajax({
                type: "POST",
                dataType: "json",
                url: "/posts/postmessage/leave/",

                data: {'operate':operate,'pmid':p,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                

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
//加载其他
function load_left_reply(p){
    var id_str='reply_message_list_'+p;
    var parent_div=document.getElementById(id_str);
    var operate="delete";
    
    var post=(window.location.pathname).replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
    // var reply_message=$('.reply_message_sign').val();
    // var pmid=$('#rep'+p).val();
    //var content=$("#intext"+p+"").val();
    //alert(content);
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    //alert(reply_message);
    $.ajax({
                type: "POST",
                dataType: "json",
                url: "/posts/postmessage/listview/"+p+'/',

                data: {'start':5,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                success: function (data) {
                    if(data.code==0){
                        var obj = eval(data.message_list);
                        alert(Math.ceil((data.message_list.length+5)/8)+1);
                        //Math.ceil((data.message_list.length+5)/8)

                        for(var i=1;i<(Math.ceil((data.message_list.length+5)/8)+1);i++){
                            document.getElementById("reply_page"+p).insertAdjacentHTML('beforeEnd','<li><a href="javascript:" onclick="reply_page('+p+','+i+')">'+i+'</a></li> ');

                        }
                        var j=1;
                        $(obj).each(function (index) {
                            if(j<4){
                            var message = obj[index];
                            parent_div.insertAdjacentHTML('beforeEnd','<div class="media" id="m'+message.id+'">\
                                <a class="media-left" href="#">\
                                    <img src="'+message.creator_avatar_url+'" alt="...">\
                                </a>\
                                <div class="media-body">\
                                    <div class="u-second-level-reply">\
                                    <input type="hidden" name="operate" value="reply">\
                                        <input type="hidden" name="post" value={{posts.id}}>\
                                        <input type="hidden" name="reply_message" class="reply_id'+message.id+'" value='+message.id+'>\
                                        <a href="#">'+message.creator+' : </a>'+message.reply_text+'\
                                    </div>\
                                </div>\
                                <div class="u-second-level-info">\
                                        <span>'+message.create_time+'</span>&nbsp;&nbsp;\
                                        <a href="javascript:;" onclick="re('+message.id+')" id="'+message.id+'"  class="inreplyButton">回复</a>\
                                        {%if user.is_superuser%}<a href="javascript:;" class="delete" onclick="del('+message.id+')">删除</a>{%endif%}\
                                </div>\
                            </div>')
                       }j++; });
                            
                    }
                },
                error: function (err) {
                    alert("err:" + err);
                }
            });

           
}
//分页
function reply_page(p,m){
    var id_str='reply_message_list_'+p;
    var parent_div=document.getElementById(id_str);
    var operate="delete";
    alert(m);
    var start=8*(m-1);
    var end=8*(m-1)+7;
    alert(start);
    alert(end);


    var post=(window.location.pathname).replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
    // var reply_message=$('.reply_message_sign').val();
    // var pmid=$('#rep'+p).val();
    //var content=$("#intext"+p+"").val();
    //alert(content);
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    //alert(reply_message);
    $.ajax({
                type: "POST",
                dataType: "json",
                url: "/posts/postmessage/listview/"+p+'/',

                data: {'start':start,'end':end,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                success: function (data) {
                    if(data.code==0){
                        $('#reply_message_list_'+p).empty();
                        var obj = eval(data.message_list);
                        
                        //Math.ceil((data.message_list.length+5)/8)

                       
                       
                        $(obj).each(function (index) {
                            
                            var message = obj[index];
                            parent_div.insertAdjacentHTML('beforeEnd','<div class="media" id="m'+message.id+'">\
                                <a class="media-left" href="#">\
                                    <img src="'+message.creator_avatar_url+'" alt="...">\
                                </a>\
                                <div class="media-body">\
                                    <div class="u-second-level-reply">\
                                    <input type="hidden" name="operate" value="reply">\
                                        <input type="hidden" name="post" value={{posts.id}}>\
                                        <input type="hidden" name="reply_message" class="reply_id'+message.id+'" value='+message.id+'>\
                                        <a href="#">'+message.creator+' : </a>'+message.content_text+'\
                                    </div>\
                                </div>\
                                <div class="u-second-level-info">\
                                        <span>'+message.time+'</span>&nbsp;&nbsp;\
                                        <a href="javascript:;" onclick="re('+message.id+')" id="'+message.id+'"  class="inreplyButton">回复</a>\
                                        {%if user.is_superuser%}<a href="javascript:;" class="delete" onclick="del('+message.id+')">删除</a>{%endif%}\
                                </div>\
                            </div>')
                        });
                            
                    }
                },
                error: function (err) {
                    alert("err:" + err);
                }
            });

           
}
//收藏
function college(){
    //alert($("#contenttxt").val());
    var operate="collect";
    var post=(window.location.pathname).replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    //alert(post);
    $.ajax({
                type: "POST",
                dataType: "json",
                url: "/posts/postmessage/leave/",

                data: {'operate':operate,'post':post,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                

                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 //alert(data.msg);
                
                window.location.reload();

      
         
  
                },
                error: function (err) {
                    alert("err:" + err);
                }
            });

           
}

function cancelcollege(){
    //alert($("#contenttxt").val());
    var operate="collect_cancel";
    var post=(window.location.pathname).replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    //alert(post);
    $.ajax({
                type: "POST",
                dataType: "json",
                url: "/posts/postmessage/leave/",

                data: {'operate':operate,'post':post,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                

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

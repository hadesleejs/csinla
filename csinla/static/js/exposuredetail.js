$(".commentnum").each(function(i,value){
    if($(this).text()>0){
        $(this).prev().text("收起回复");
        $(this).prev().css({
            "border": "2px solid #dfdfdf",
            "border-bottom": "10px solid white"
        });
        $(this).nextAll(".u-reply").show();
    }
});
var hash=window.location.hash.replace(/^[^\d]*(\d+)[^\d]*$/, "$1");

if((window.location.href).indexOf("#")>-1){
    $("#m"+hash).parents('.u-reply').show();
    window.location.href="#m"+hash;
}
else{
     $("#m"+hash).parents('.u-reply').hide();
}
$(function($) {
    
    $('.mobile-nav-btn').click(function(e) {
        e.preventDefault();
        $('.user').slideDown();
    });
    $('.remove-nav').click(function(e) {
        e.preventDefault();
        $('.user').slideUp();
    });
    $('.has-sub-item').click(function(e) {
        e.preventDefault();
        $(this).next('.home-nav-sub-item').slideToggle();
    });
});
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
//发表评论
$("#publish").click(function(){
    //alert($("#contenttxt").val());
    var operate="reply";
     var content=$(".emo").val();
     //alert(content);
     var content_image="";
     //alert($("#contenttxt").html());
    
   if ($("#contenttxt").html()==""||$("#contenttxt").html()==null) {
    content_image=""; 
    //alert(content_image);
    //alert(image);
    // alert(content1);
    }
    else{
        for (var i = 0; i < document.getElementById("contenttxt").getElementsByTagName("img").length; i++) {
           //alert(document.getElementById("contenttxt").getElementsByTagName("img")[i].src);
        content_image+=document.getElementById("contenttxt").getElementsByTagName("img")[i].src+"$$$$$";}
        //alert(content_image);
        }
    if ($("#contenttxt").html()=="" && $(".emo").val()=="") {
        alert("请填写评论");

    }
    else{
    var post=(window.location.pathname).replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
    var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    //alert(post);
    $.ajax({
                type: "POST",
                dataType: "json",
                url: "/posts/postmessage/leave/",
                data: {'operate':operate,'post':post,'content_image':content_image,'content':content,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 alert(data.msg);
                
                window.location.reload()
      
         
  
                },
                error: function (err) {
                    alert("err:" + err);
                }
            });}
           
});
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
                                        {% if user.is_superuser %}<a href="javascript:;" class="delete" onclick="del('+message.id+')">删除</a>{% endif %}\
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
                 alert(data.msg);
                
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
        $('.emotion').bind({
            click: function(event){
                if(! $('#sinaEmotion').is(':visible')){
                    $(this).parseEmotion();
                    event.stopPropagation();
                }
               
            }
        });
       
       function mre(mi){
    // var rp=$(this).arr('id');
    // alert(rp);
    $(".reply_message_sign").val(mi);
   //$("#intext").val("回复");
   // $(".ff textarea").addClass("intext"+i);
}
//回复
function mpli(mp){
    var operate="reply";
    
    var post=(window.location.pathname).replace(/^[^\d]*(\d+)[^\d]*$/, "$1");
    var reply_message=$('#mrep'+mp).val();
    var content=$("#mintext"+mp+"").val();
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
//删除
function mdel(mp){
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
                data: {'operate':operate,'pmid':mp,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
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
function mload_left_reply(mp){
    var id_str='mreply_message_list_'+mp;
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
                url: "/posts/postmessage/listview/"+mp+'/',
                data: {'start':5,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                success: function (data) {
                    if(data.code==0){
                        var obj = eval(data.message_list);
                        alert(Math.ceil((data.message_list.length+5)/8)+1);
                        //Math.ceil((data.message_list.length+5)/8)
                        for(var i=1;i<(Math.ceil((data.message_list.length+5)/8)+1);i++){
                            document.getElementById("mreply_page"+mp).insertAdjacentHTML('beforeEnd','<li><a href="javascript:" onclick="mreply_page('+mp+','+i+')">'+i+'</a></li> ');
                        }
                        var j=1;
                        $(obj).each(function (index) {
                            if(j<4){
                            var message = obj[index];
                            parent_div.insertAdjacentHTML('beforeEnd','<div class="media" id="mm'+message.id+'">\
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
                                        <a href="javascript:;" onclick="mre('+message.id+')" id="m'+message.id+'"  class="inreplyButton">回复</a>\
                                        {%if user.is_superuser%}<a href="javascript:;" class="delete" onclick="mdel('+message.id+')">删除</a>{%endif%}\
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
function mreply_page(p,m){
    var id_str='mreply_message_list_'+p;
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
                        $('#mreply_message_list_'+p).empty();
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
                 alert(data.msg);
                
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
     
     $(".carousel-inner").click(function(){
        $(".carousel").hide();
    });
     
     function carousel(){
    $("#myCarousel").show();
  }
    function mcarousel(){
    $("#mmyCarousel").show();
     
     
    /******/ (function(modules) { // webpackBootstrap
/******/  // The module cache
/******/  var installedModules = {};
/******/
/******/  // The require function
/******/  function __webpack_require__(moduleId) {
/******/
/******/    // Check if module is in cache
/******/    if(installedModules[moduleId])
/******/      return installedModules[moduleId].exports;
/******/
/******/    // Create a new module (and put it into the cache)
/******/    var module = installedModules[moduleId] = {
/******/      exports: {},
/******/      id: moduleId,
/******/      loaded: false
/******/    };
/******/
/******/    // Execute the module function
/******/    modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/    // Flag the module as loaded
/******/    module.loaded = true;
/******/
/******/    // Return the exports of the module
/******/    return module.exports;
/******/  }
/******/
/******/
/******/  // expose the modules object (__webpack_modules__)
/******/  __webpack_require__.m = modules;
/******/
/******/  // expose the module cache
/******/  __webpack_require__.c = installedModules;
/******/
/******/  // __webpack_public_path__
/******/  __webpack_require__.p = "/";
/******/
/******/  // Load entry module and return exports
/******/  return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ 
/* 1 */
/***/ function(module, exports, __webpack_require__) {


  $( function() {
  // Swipe
  (function() {
    new Hammer( $( "#mmyCarousel")[ 0 ], {
      domEvents: true
    } );
   
    $( "#mmyCarousel").on( "swipeleft", function( e ) {
    $("#mmyCarousel").carousel('next')
    } );
    
    $( "#mmyCarousel").on( "swiperight", function( e ) {
     $("#mmyCarousel").carousel('prev')
    } );
  } )();
  
 
 
 
  // Hammer Time

} );
  /**
  * kind of messy code, but good enough for now
  */
  // polyfill


  
  

  

  




/***/ },
/* 2 */
/***/ 
/******/ ])
}   
         
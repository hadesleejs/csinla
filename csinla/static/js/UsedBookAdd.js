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
    new Hammer( $( "#myCarousel2" )[ 0 ], {
      domEvents: true
    } );
    var current = 0;
    var imgs = $( "#carousel-inner2.item" );
    var pages = $( "#carousel-indicators2 li" );
    $( "#myCarousel2" ).on( "swipeleft", function( e ) {
    $('#myCarousel2').carousel('next')
    } );
    $( "#myCarousel2" ).on( "swiperight", function( e ) {
     $('#myCarousel2').carousel('prev')
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
  $('.upload_delete').click(function(){
     $(this).parent("li.upload_append_list").remove();
     hh=$("#dd").html();
   });
  $('.mupload_delete').click(function(){
     $(this).parent("li.mupload_append_list").remove();
     hh1=$("#dd3").html();
   });
   function showinput(){
  if($(":radio[name='district1']:checked").val()=="OTHER"){
    $('#loc5txt').css('display','inline-block');
  }
  else{
    var district=$(":radio[name='district1']:checked").val();
    $('#loc5txt').hide();
   $('#loc5txt').val(district);
 
  }
}
var hh=$("#dd").html();
var hh1=$("#dd3").html();
function convertImgToBase64(url, callback, outputFormat){ 
var canvas = document.createElement('CANVAS'); 
var ctx = canvas.getContext('2d'); 
var img = new Image; 
img.crossOrigin = 'Anonymous'; 
img.onload = function(){ 
canvas.height = img.height; 
canvas.width = img.width; 
ctx.drawImage(img,0,0,img.width, img.height); 
var dataURL = canvas.toDataURL('image/png'); 
callback.call(this, dataURL); 
// Clean up 
canvas = null; 
}; 
img.src = url; 
} 
var imagepu=[];
          
 for (var i = 0; i < $(".upload_image").length; i++) {
        //alert($(".upload_image")[i].src);
        var imageUrl = $(".upload_image")[i].src;
        console.log('imageUrl', imageUrl); 
        convertImgToBase64(imageUrl, function(base64Img){ 
          
        imagepu.push(base64Img);
        

}); 
        }
var mimagepu=[];
          
 for (var i = 0; i < $(".mupload_image").length; i++) {
        //alert($(".upload_image")[i].src);
        var imageUrl = $(".mupload_image")[i].src;
        console.log('imageUrl', imageUrl); 
        convertImgToBase64(imageUrl, function(base64Img){ 
          
        mimagepu.push(base64Img);
        

}); 
        }
        

function selectother(){
     var a= $('#mlocal option:selected');
    
    if (a.val()=="OTHER") {
      $('#mlocaltxt').show();
      $('#mlocal').hide();
    }
    else{
      var mloc=a.val();
      $('#mlocaltxt').val(mloc);    }
    
  }
var params = {
   fileInput: $("#avatar-selector").get(0),
  //dragDrop: $("#fileDragArea").get(0),
   upButton: $("#titi").get(0),
   url: $("#feo").attr("action"),
  filter: function(files) {
    var arrFiles = [];
    for (var i = 0, file; file = files[i]; i++) {
      if (file.type.indexOf("image") == 0 && i<9) {
        // if (file.size >= 3512000) {
        //   alert('您这张"'+ file.name +'"图片大小过大，应小于500k');  
        // } else {
          arrFiles.push(file);  
        // }     
      } else {
       
      }
    }
    return arrFiles;
  },
  onSelect: function(files) {
    var html = '', i = 0;
    $("#dd").html('<div class="upload_loading"></div>');
    var funAppendImage = function() {
      file = files[i];
      if (file&&i<9) {
        var reader = new FileReader()
        reader.onload = function(e) {
          html = html + '<li id="uploadList_'+ i +'" class="upload_append_list">'+ 
            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage('+i+')" data-index="'+ i +'"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +
            '<img id="uploadImage_' + i + '" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 
             
          '</li>';
          
          i++;
          funAppendImage();

        }
       
        reader.readAsDataURL(file);
      } else {
        $("#dd").html(hh+html);
        var num=9-i;
        $("#dd1").html("还可以上传"+num+"张");

        if (html) {
          //删除方法
          $(".upload_delete").click(function() {
            ZXXFILE.funDeleteFile(files[parseInt($(this).attr("data-index"))]);
            return false; 
          });
          //提交按钮显示
          //$("#fileSubmit").show();  
        } else {
          //提交按钮隐藏
         // $("#fileSubmit").hide();  
        }
      }
    };
    funAppendImage();   
  },
  onDelete: function(file) {
    $("#uploadList_" + file.index).fadeOut();
  },
  onDragOver: function() {
    $(this).addClass("upload_drag_hover");
  },
  onDragLeave: function() {
    $(this).removeClass("upload_drag_hover");
  },
  onProgress: function(file, loaded, total) {
    // var eleProgress = $("#uploadProgress_" + file.index), percent = (loaded / total * 100).toFixed(2) + '%';
    // eleProgress.show().html(percent);
  },
  onSuccess: function(file, response) {
   // $("#uploadInf").append("<p>上传成功，图片地址是：" + response + "</p>");
  },
  onFailure: function(file) {
   // $("#uploadInf").append("<p>图片" + file.name + "上传失败！</p>");  
   // $("#uploadImage_" + file.index).css("opacity", 0.2);
  },
  //onComplete: function() {
    //提交按钮隐藏
    //$("#fileSubmit").hide();
    //file控件value置空
   // $("#fileImage").val("");
    //$("#uploadInf").append("<p>当前图片全部上传完毕，可继续添加上传。</p>");
  //}
};
ZXXFILE = $.extend(ZXXFILE, params);
ZXXFILE.init();
function mdelimage(mimagenum){
  $("#muploadList_"+mimagenum).remove();
}
function delimage(imagenum){
  $("#uploadList_"+imagenum).remove();
}
var params1 = {
  fileInput: $("#avatar-selector1").get(0),
  //dragDrop: $("#fileDragArea").get(0),
   upButton: $("#titi").get(0),
   url: $("#feo").attr("action"),
  filter: function(files) {
    var arrFiles = [];
    for (var i = 0, file; file = files[i]; i++) {
      if (file.type.indexOf("image") == 0 && i<9) {
        // if (file.size >= 3512000) {
        //   alert('您这张"'+ file.name +'"图片大小过大，应小于500k');  
        // } else {
          arrFiles.push(file);  
        // }     
      } else {
       
      }
    }
    return arrFiles;
  },
  onSelect: function(files) {
    var html1 = '', i = 0;
    $("#dd").html('<div class="upload_loading"></div>');
    var funAppendImage1 = function() {
      file = files[i];
      if (file&&i<9) {
        var reader = new FileReader()
        reader.onload = function(e) {
          html1 = html1 + '<li id="muploadList_'+ i +'" class="mupload_append_list">'+ 
            '<a href="javascript:" class="mupload_delete" title="删除"  onclick="mdelimage('+i+')" data-index="'+ i +'"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +
            '<img id="muploadImage_' + i + '" src="' + e.target.result + '" class="mupload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 
             
          '</li>';
          
          i++;
          funAppendImage1();

        }
       
        reader.readAsDataURL(file);
      } else {
        $("#dd3").html(hh1+html1);
        var num=9-i;
        $("#upnumber").html("还可以上传"+num+"张");

        if (html1) {
          //删除方法
          $(".mupload_delete").click(function() {
            ZXXFILE1.funDeleteFile(files[parseInt($(this).attr("data-index"))]);
            return false; 
          });
          //提交按钮显示
          //$("#fileSubmit").show();  
        } else {
          //提交按钮隐藏
         // $("#fileSubmit").hide();  
        }
      }
    };
    funAppendImage1();   
  },
  onDelete: function(file) {
    $("#muploadList_" + file.index).fadeOut();
  },
  onDragOver: function() {
    $(this).addClass("upload_drag_hover");
  },
  onDragLeave: function() {
    $(this).removeClass("upload_drag_hover");
  },
  onProgress: function(file, loaded, total) {
    // var eleProgress = $("#uploadProgress_" + file.index), percent = (loaded / total * 100).toFixed(2) + '%';
    // eleProgress.show().html(percent);
  },
  onSuccess: function(file, response) {
   // $("#uploadInf").append("<p>上传成功，图片地址是：" + response + "</p>");
  },
  onFailure: function(file) {
   // $("#uploadInf").append("<p>图片" + file.name + "上传失败！</p>");  
   // $("#uploadImage_" + file.index).css("opacity", 0.2);
  },
  //onComplete: function() {
    //提交按钮隐藏
    //$("#fileSubmit").hide();
    //file控件value置空
   // $("#fileImage").val("");
    //$("#uploadInf").append("<p>当前图片全部上传完毕，可继续添加上传。</p>");
  //}
};
ZXXFILE1 = $.extend(ZXXFILE1, params1);
ZXXFILE1.init();


    function math(n){
      if(!$("#price_"+n).val().match(/^(:?(:?\d+))$/)){//(/^(:?(:?\d+.\d+)|(:?\d+))$/))
       $("#price_"+n).val(null);
       $("#price_"+n).focus();
       }
    }
    function mmath(m){
      if(!$("#mprice_"+m).val().match(/^(:?(:?\d+))$/)){//(/^(:?(:?\d+.\d+)|(:?\d+))$/))
       $("#mprice_"+m).val(null);
       $("#mprice_"+m).focus();
       }
    }
    //alert($("#book_detail_str").val());
  //  var i=1;
  //   var g=1;
  //   var z=1;
  //   for(z=1;z<5;z++){
  //   if($("#div_"+z).val()!=null){
  //      document.getElementById('addtxt').insertAdjacentHTML('beforeEnd','<input type=text id=div_'+i+' style=width:10%;margin-left:10px;value="" name='+i+' ><input type=button id=dele_'+i+' name='+i+' value=删除 onclick=del('+i+')>');
  //      z++;
  //   }
  // }
  //  function add(){

  //   if(g<5) {
  //   document.getElementById('addtxt').insertAdjacentHTML('beforeEnd','<input type=text id=div_'+i+' style=width:10%;margin-left:10px; name='+i+' ><input type=button id=dele_'+i+' name='+i+' value=删除 onclick=del('+i+')>');
  //   document.getElementById('addprice').insertAdjacentHTML('beforeEnd','<input class=pri onkeyup="math()" type=text id=price_'+i+' style=width:10%;margin-left:10px;  name='+i+' >');
  //   document.getElementById('addisbn').insertAdjacentHTML('beforeEnd','<input name="text" id="isbn_'+i+'" name="text_'+i+'" type="text" value="" style="width:100%;margin-top:20px;"  />');
  //     i++;
  //     g++;
  // }
  // else{alert("最多只能添加5件商品");}
   
  // }
//判断两个单选组被选中的值是否等于空
// if($('#birthday').text())
// if($(":radio[name='r1']:checked").val()==null)
// alert("有题目为空，请补充完整");
// else
// document.location.href="https://123.sogou.com/";
// })
var i = 1;
     function add(){
    $("#myCarousel").carousel('pause');
    if (i<10) {
  document.getElementById("carousel-indicators").insertAdjacentHTML('beforeEnd','<li data-target="#myCarousel" data-slide-to="'+i+'" id="li_'+i+'" style="margin-bottom: -40px;background-color:#000"></li>');
  document.getElementById("carousel-inner").insertAdjacentHTML('beforeEnd','<div id="div_'+i+'" class="item"><div class="edit-content-form" style="clear:both"> <label class="checkbox check-title" style="text-align:center;margin-top:-5px"><span style="color:red">*</span>书籍名称：</label><input type="text" class="name_text div_" value="" style="width:35%;margin-left:0px;margin-top:5px;"><a href="javascript:"><img src="/static/images/add.png" onclick="add()"></a><a href="javascript:"><img src="/static/images/useddel.png" onclick="del('+i+')"></a><input type="text" class="iddd" id="inp_'+i+'"  style="display:none"></div><div class="edit-content-form" style="clear:both"><label class="checkbox check-title" style="text-align:center;margin-top:-5px"><span style="color:red">*</span>商品价格：</label><input type="text" class="pri price_" onkeyup="math('+i+')" id="price_'+i+'" value="" style="width:10%;margin-left:0px;margin-top:5px;"></div><div class="edit-content-form" style="clear:both"><label class="checkbox check-title" style="text-align:center;margin-top:-5px;margin-left: 8px;">ISBN：</label><input type="text" placeholder="选填项" class="isbn_text isbn_" value="" style="width:35%;margin-left:27px;margin-top:5px;"></div></div>');
   i = i + 1;
   $('#myCarousel').carousel('next')
}
else{
  alert("最多只能添加10件商品")
}}
mi = 1;
     function madd(){
    $("#myCarousel2").carousel('pause');
    if (mi<10) {
  document.getElementById("carousel-indicators2").insertAdjacentHTML('beforeEnd','<li id="mli_'+mi+'" data-target="#myCarousel2" data-slide-to="'+mi+'" style="margin-bottom: -40px;background-color:#000"></li>');
  document.getElementById("carousel-inner2").insertAdjacentHTML('beforeEnd','<div id="mdiv_'+mi+'" class="item"><div class="m-edit-content-form" style="clear:both;"><label class="checkbox check-title" style="font-family:"微软雅黑";font-size:18px;text-align:center;"><span style="color:red">*</span>书籍名称：</label><input type="text" class="name_text mdiv_" style="width:50%;margin-left:3px;margin-top:20px;height:30px;" value=""><span id="addtxt"></span><a href="javascript:"><img src="/static/images/add.png" onclick="madd()"></a><a href="javascript:"><img src="/static/images/useddel.png" onclick="mdel('+mi+')"></a><input type="text" class="middd" id="minp_'+mi+'"  style="display:none"></div><div class="m-edit-content-form" style="clear:both;"> <label class="checkbox check-title" style="font-family:"微软雅黑";font-size:18px;text-align:center;"><span style="color:red">*</span>书籍价格：</label><input type="text" class="pri mprice_" onkeyup="mmath('+mi+')" id="mprice_'+mi+'" style="width:50%;margin-left:3px;margin-top:20px;height:30px;" value=""></div><div class="m-edit-content-form" style="clear:both;"><label class="checkbox check-title" style="font-family:"微软雅黑";font-size:18px;text-align:center;"><span style="color:red">&nbsp;</span>ISBN：</label><input type="text" placeholder="选填项" class="isbn_text misbn_" style="width:50%;margin-left:3px;margin-top:20px;height:30px;font-size:14px;color:#000" value="" style="width:35%;margin-left:27px;margin-top:5px;"></div></div>');
   mi = mi + 1;
   $('#myCarousel2').carousel('next')
}
else{
  alert("最多只能添加10件商品")
}}
$(function($) {

    
    $('#birthday').flatpickr({
      
         minDate:"today",
         enableTime:false,
      //   onClose:function(dateObj,dateStr,instance){
      //   alert($('#birthday').val())
      // }
         maxDate:new Date().fp_incr(90)
         
        });
     $('#birthday4').flatpickr({
          minDate:"today",
         enableTime:false,
      //   onClose:function(dateObj,dateStr,instance){
      //   alert($('#birthday').val())
      // }
         maxDate:new Date().fp_incr(90)
         
        });
     $('#birthday5').flatpickr({
         //  disable:[
         // {
         //  from:"today",
         //  to:new Date().fp_incr(60)
         // }
         // ]
        });
     $('#birthday6').flatpickr({
          
        });
      $('#birthday7').flatpickr({
          
        });
     $('#birthday8').flatpickr({
          
        });

     if($('#loc5txt').val()!="None" && $(":radio[name='district1']:checked").val()==null){
    $(":radio[name='district1']").attr("checked","OTHER");
    $('#loc5txt').show();
   }
    if($('#mlocaltxt').val()!="None" && $('#mlocal option:selected').val()=="select"){
    $('#mlocal option:selected').val("OTHER");
    $('#mlocal').hide();
    $('#mlocaltxt').show();
   }
});

   
    if(screen.width<768){
     $("#pcxx").remove();
     $("#edui1").css("width","300px");
    }
   /* i = 1;
    function add(){
    if (i<5) {
        document.getElementById("detail_list").innerHTML+='<li class="detail_item" style="float:left">\
                        <div class="detail_item_part">\
                           \
                            <input type="text" class="name_text" value="" style="width:51%;margin-left:11px;margin-top:10px;">\
                        </div>\
                        <div class="detail_item_part">\
                            \
                            <input type="text" class="price_text" value="" style="width:51%;margin-left:11px;margin-top:5px;">\
                        </div>\
                        <div class="detail_item_part">\
                            \
                            <input type="text" class="isbn_text" value="" style="width:51%;margin-left:11px;margin-top:5px;">\
                        </div>\
                    </li>'
        i = i + 1;
    }
    else{
        alert("最多只能添加5件商品")
    }
}*/

function del(o){
  $('#myCarousel').carousel('prev');
 document.getElementById("carousel-inner").removeChild(document.getElementById("div_"+o));
 document.getElementById("carousel-indicators").removeChild(document.getElementById("li_"+o));
i=i-1;

}
function mdel(mo){
  $('#myCarousel2').carousel('prev');
 document.getElementById("carousel-inner2").removeChild(document.getElementById("mdiv_"+mo));
 document.getElementById("carousel-indicators2").removeChild(document.getElementById("mli_"+mo));

mi=mi-1;
}



$("#push1").click(function(){



  var bookid1;
  var bookid=[];
 
 if($(".iddd1").length>0){
  bookid1= $(".iddd1").val();
 }
 else{
  bookid1=0;
 }
  var shu=[];

  var shu1=[];
   var shu2=[];
   var bookname = $("#bookname").val()
     var price=$("#price").val();
      var isbn=$("#ISBN").val();
     var bb;
$(".div_").each(function(i,value){
  //alert($(this).val());
shu.push(value.value);
$(".price_").each(function(j,value1){
shu1.push(value1.value);
$(".isbn_").each(function(k,value2){
shu2.push(value2.value);
$(".iddd").each(function(t,value3){
bookid.push(value3.value);

  });
  });
  });
if (bookid[i]=="") {
  bookid[i]=0;
}

//alert(bookid);
bb+="~#~"+shu[i]+"~*~"+shu1[i]+"~*~"+shu2[i]+"~*~"+bookid[i];
//alert(bb);
});

   var book_detail_str=bookname+"~*~"+price+"~*~"+isbn+"~*~"+bookid1+bb;
book_detail_str=book_detail_str.replace("undefined","");
//alert(book_detail_str);
   /* var book_detail_str='',
    book_item_str='';
    // alert('0000');
    $('#detail_list .detail_item').each(function(){
        book_item_str='';
        $(this).children('.detail_item_part').each(function(){
            // alert($(this).find('input').val());
            book_item_str+=$(this).find('input').val()+':';
            // alert('1111:'+book_item_str);
        });
        book_detail_str+=book_item_str+'-';
        // alert('2222:'+book_item_str);
    });*/
    // alert(book_detail_str);
   

    if($('#title').val()==""){
      alert("标题是必填项");
      $('#title').focus();
       return false;
     }
     else if($('#title').val().length>30){
      alert("标题过长，请限制在30字以内");
      $('#title').focus();
       return false;
     }
     else if($('#bookname').val()==""){
      alert("书籍名称是必填项");
      $('#bookname').focus();
       return false;
     }


     else if($('#bookname').val().length>64){
      alert("书籍名称过长，请限制在64字以内");

      $('#bookname').focus();
       return false;
     }
    else if($('#price').val()==""){
      alert("商品价格是必填项");
      $('#price').focus();
       return false;
     }
      else if(!$('#price').val().match(/^(:?(:?\d+))$/)){//(/^(:?(:?\d+.\d+)|(:?\d+))$/))
       alert('价格请填写整数');
       $('#price').focus();
       return false;
     }
     // else if($('#isbn').val()==""){
     //  alert("ISBN是必填项");
     //  $('#isbn').focus();
     //   return false;
     // }

     // else if($('#isbn').val()!=''&& !$('#ISBN').val().match(/^(:?(:?\d+\w+)|(:?\w+)|(:?\d+))$/)){//(/^(:?(:?\d+.\d+)|(:?\d+))$/))
     //   alert("ISBN只能填写英文、数字");
     //  $('#isbn').focus();
     //   return false;
     // }

     else if($(":radio[name='district1']:checked").val()==null){
      alert("地区是必填项");
       return false;
     }
     else if($(":radio[name='district1']:checked").val()=="OTHER" && $('#loc5txt').val()==""){
      alert("地区是必填项");
       return false;
     }
    
      
     else if($('#connect_name').val()==""){
      alert("联系人是必填项");
       return false;
     }
     else if($('#connect_phone').val()==""){
      alert("联系电话是必填项");
       return false;
     }
      else if($('#connect_wx').val()==""){
      alert("微信是必填项");
      return false;
     }

        else{ 

          var title=$('#title').val();
          var book_detail_str=book_detail_str;
          var district=$('#loc5txt').val();
          var connect_name=$('#connect_name').val();
          var connect_phone=$('#connect_phone').val();
          var connect_wx=$('#connect_wx').val();
          var connect1=$('#myEditor').val();
          var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
          // alert(title);
          // alert(goods_detail_str1);
          // alert(district);
          // alert(connect_name);
          // alert(connect_wx);
          var image1="";
         for (var i = 0; i < $(".upload_image").length; i++) {
        //alert($(".upload_image")[i].src);
        var Cnv = document.getElementById('myCanvas');
            var Cntx = Cnv.getContext('2d');//获取2d编辑容器
            var imgss =   new Image();
           
              
                    url = $(".upload_image")[i].src;
                    imgss.src = url;
                 
                       //等比缩放
                        var m = imgss.width / imgss.height;
                         Cnv.height =300;//该值影响缩放后图片的大小
                         Cnv.width= 300*m ;
                        //img放入画布中
                        //设置起始坐标，结束坐标
                        Cntx.drawImage($(".upload_image")[i], 0, 0,300*m,300);
                        var Pic = document.getElementById("myCanvas").toDataURL("image/png");
            $(".upload_image")[i].src =Pic ;
            //上传
            // 去除多余，得到base64编码的图片字节流
            Pic = Pic.replace(/^data:image\/(png|jpg);base64,/, "");
        if (new RegExp('http:').test($(".upload_image")[i].src)) {
          //alert($(".upload_image").length);
          console.log(imagepu[i]);
          image1+=imagepu[i]+"$$$$$";
        }
        else{
        image1 +=$(".upload_image")[i].src+"$$$$$";}}
          $("#push1").attr({"disabled":"disabled"});
  
  //alert($(".upload_image").length);
  
         $.ajax({
                type: "POST",
                dataType: "json",
                url: "",
                 traditional: true,
                data: {'title':title,'book_detail_str':book_detail_str,'district':district,'connect_name':connect_name,'connect_phone':connect_phone,'connect_wx':connect_wx,'content':connect1,'image':image1,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 // alert(data.post_id);
                
                if(data.code==0 && data.post_id>0){
                window.location.href="/posts/complete/"+data.post_id+"";}
                else{
                  alert(data.msg);
                  $('#push1').removeAttr("disabled");
                }
      
  
                },
                error: function (err) {
                    alert("err:" + err);
                    $('#push1').removeAttr("disabled");
                }
            });
         }
     /* else if($('#myEditor').val()==""){
      alert("详细内容是必填项");
     }*/
     
   });
     $("#push2").click(function(){


        var mbookid1;
  var mbookid=[];
 
 if($(".middd1").length>0){
  mbookid1= $(".middd1").val();
 }
 else{
  mbookid1=0;
 }
  var mshu=[];

  var mshu1=[];
   var mshu2=[];
   var mbookname = $("#mbookname").val()
     var mprice=$("#mprice").val();
      var misbn=$("#mISBN").val()
     var mbb;
$(".mdiv_").each(function(mi,value4){
  //alert($(this).val());
mshu.push(value4.value);
$(".mprice_").each(function(mj,value5){
mshu1.push(value5.value);
$(".misbn_").each(function(mk,value6){
mshu2.push(value6.value);
$(".middd").each(function(mt,value7){
mbookid.push(value7.value);

  });
  });
  });
if (mbookid[mi]=="") {
  mbookid[mi]=0;
}

//alert(shu);
mbb+="~#~"+mshu[mi]+"~*~"+mshu1[mi]+"~*~"+mshu2[mi]+"~*~"+mbookid[mi];
//alert(bb);
});

   var mbook_detail_str=mbookname+"~*~"+mprice+"~*~"+misbn+"~*~"+mbookid1+mbb;
mbook_detail_str=mbook_detail_str.replace("undefined","");
//alert(mbook_detail_str);
   /* var book_detail_str='',
    book_item_str='';
    // alert('0000');
    $('#detail_list .detail_item').each(function(){
        book_item_str='';
        $(this).children('.detail_item_part').each(function(){
            // alert($(this).find('input').val());
            book_item_str+=$(this).find('input').val()+':';
            // alert('1111:'+book_item_str);
        });
        book_detail_str+=book_item_str+'-';
        // alert('2222:'+book_item_str);
    });*/
     //alert(book_detail_str);
    $("#mbook_detail_str").val(mbook_detail_str);
      
     if($('#mtitle').val()==""){

      alert("标题是必填项");
      return false;
     }
     
      else if($('#mbookname').val()==""){

      alert("书籍名称是必填项");
      return false;
     }
     else if($('#mprice').val()==""){

      alert("书籍价格是必填项");
      return false;
     }
    
     else if ($('#mlocal option:selected').val()=="select") {
      alert("地区是必填项");
      return false;
     }
      
     else if($('#mconnect_name').val()==""){
      alert("联系人是必填项");
      return false;
     }
     else if($('#mconnect_phone').val()==""){
      alert("联系电话是必填项");
      return false;
     }
      else if($('#mconnect_wx').val()==""){
      alert("微信是必填项");
      return false;
     }
    
     // else if($('.mmyEditor').val()==""){
     //  alert("详细内容是必填项");
     //  return false;
     // }
 else{var mtitle=$('#mtitle').val();
          var mbook_detail_str=mbook_detail_str;
          var mdistrict=$('#mlocaltxt').val();
          var mconnect_name=$('#mconnect_name').val();
          var mconnect_phone=$('#mconnect_phone').val();
          var mconnect_wx=$('#mconnect_wx').val();
          var mconnect1=$('#mmyEditor').val();
          var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
          // alert(title);
          // alert(goods_detail_str1);
          // alert(district);
          // alert(connect_name);
          // alert(connect_wx);
          var mimage1="";

         for (var i = 0; i < $(".mupload_image").length; i++) {
        //alert($(".upload_image")[i].src);
        var Cnv = document.getElementById('myCanvas');
            var Cntx = Cnv.getContext('2d');//获取2d编辑容器
            var imgss =   new Image();
           
              
                    url = $(".mupload_image")[i].src;
                    imgss.src = url;
                 
                       //等比缩放
                        var m = imgss.width / imgss.height;
                         Cnv.height =300;//该值影响缩放后图片的大小
                         Cnv.width= 300*m ;
                        //img放入画布中
                        //设置起始坐标，结束坐标
                        Cntx.drawImage($(".mupload_image")[i], 0, 0,300*m,300);
                        var Pic = document.getElementById("myCanvas").toDataURL("image/png");
            $(".mupload_image")[i].src =Pic ;
            //上传
            // 去除多余，得到base64编码的图片字节流
            Pic = Pic.replace(/^data:image\/(png|jpg);base64,/, "");
        if (new RegExp('http:').test($(".mupload_image")[i].src)) {
          //alert($(".upload_image").length);
          console.log(mimagepu[i]);
          mimage1+=mimagepu[i]+"$$$$$";
        }
        else{
        mimage1 +=$(".mupload_image")[i].src+"$$$$$";}}
          $("#push2").attr({"disabled":"disabled"});
  
  //alert($(".mupload_image").length);
  
         $.ajax({
                type: "POST",
                dataType: "json",
                url: "",
                 traditional: true,
                data: {'title':mtitle,'book_detail_str':mbook_detail_str,'district':mdistrict,'connect_name':mconnect_name,'connect_phone':mconnect_phone,'connect_wx':mconnect_wx,'content':mconnect1,'image':mimage1,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 // alert(data.post_id);
                
                if(data.code==0 && data.post_id>0){
                window.location.href="/posts/complete/"+data.post_id+"";}
                else{
                  alert(data.msg);
                  $('#push2').removeAttr("disabled");
                }
      
         
  
                },
                error: function (err) {
                    alert("err:" + err);
                    $('#push2').removeAttr("disabled");
                }
            });
         
   }
   });
 
   
   
     
   $('#id_tags').addClass('form-control');
    $('#id_tags').css('width','35%');
    $('#id_tags').css('margin-left','110px');
    $('#id_tags').css('margin-bottom','17px');
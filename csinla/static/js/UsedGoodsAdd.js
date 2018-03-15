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
var hh=$("#dd").html();
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
var params = {
  fileInput: $("#avatar-selector").get(0),
  //dragDrop: $("#fileDragArea").get(0),
   upButton: $("#titi").get(0),
   url: $("#feo").attr("action"),
  filter: function(files) {
    imagesrc=files;
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
       // $("#dd").html(html);
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
 $('.upload_delete').click(function(){
     $(this).parent("li.upload_append_list").remove();
     hh=$("#dd").html();
   });
  $('.mupload_delete').click(function(){
     $(this).parent("li.mupload_append_list").remove();
     hh1=$("#dd3").html();
   });
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


    //下面用于多图片上传预览功能

    function setImagePreviews(avalue) {

        var docObj = document.getElementById("avatar-selector1");

        var dd3 = document.getElementById("dd3");

        dd3.innerHTML = "";

        var fileList = docObj.files;

        for (var i = 0; i < 9; i++) {            



            dd3.innerHTML += "<li style='float:left;margin-top:30px' > <img id='img" + i + "'  /> </li>";

            var imgObjPreview = document.getElementById("img"+i); 
            if(i<8){
            var nu=9-i;
            document.getElementById("upnumber").innerHTML="还可以上传"+nu+"张";}
            else{
              var nu=8-i;
            document.getElementById("upnumber").innerHTML="还可以上传"+nu+"张";
          }
            
            

            if (docObj.files && docObj.files[i]) {

                //火狐下，直接设img属性

                imgObjPreview.style.display = 'block';

                imgObjPreview.style.width = '100%';

                imgObjPreview.style.height = '100%';

                //imgObjPreview.src = docObj.files[0].getAsDataURL();

                //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式

                imgObjPreview.src = window.URL.createObjectURL(docObj.files[i]);

            }

            else {

                //IE下，使用滤镜

                docObj.select();

                var imgSrc = document.selection.createRange().text;

                alert(imgSrc)

                var localImagId = document.getElementById("img" + i);

                //必须设置初始大小

                localImagId.style.width = "100%";

                localImagId.style.height = "100%";

                //图片异常的捕捉，防止用户修改后缀来伪造图片

                try {

                    localImagId.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale)";

                    localImagId.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = imgSrc;

                }

                catch (e) {

                    alert("您上传的图片格式不正确，请重新选择!");

                    return false;

                }

                imgObjPreview.style.display = 'none';

                document.selection.empty();


            }

        }  



        return true;

    }




    <!-- <script>
    //上传图片选择文件改变后刷新预览图
    $("#avatar-selector").change(function(e){
    //获取目标文件
    var file = e.target.files||e.dataTransfer.files;
    //如果目标文件存在
    if(file){
        //定义一个文件阅读器
        var reader = new FileReader();
        //文件装载后将其显示在图片预览里
        reader.onload=function(){
            $("#img_preview").attr("src", this.result);
        }
        //装载文件
        reader.readAsDataURL(file[0]);
    }
    });
    
    
    //下面用于多图片上传预览功能
    
    function setImagePreviews(avalue) {
    
        var docObj = document.getElementById("avatar-selector1");
    
        var dd3 = document.getElementById("dd3");
    
        dd3.innerHTML = "";
    
        var fileList = docObj.files;
    
        for (var i = 0; i < 10; i++) {            
    
          if(i<9){
    
            dd3.innerHTML += "<li style='float:left;margin-top:30px' > <img id='img" + i + "'  /> </li>";
    
            var imgObjPreview = document.getElementById("img"+i); 
            if(i<8){
            var nu=9-i;
            document.getElementById("upnumber").innerHTML="还可以上传"+nu+"张";}
            else{
              var nu=8-i;
            document.getElementById("upnumber").innerHTML="还可以上传"+nu+"张";
          
            }}
            else{alert('只能上传9张');}
            
    
            if (docObj.files && docObj.files[i]) {
    
                //火狐下，直接设img属性
    
                imgObjPreview.style.display = 'block';
    
                imgObjPreview.style.width = '100%';
    
                imgObjPreview.style.height = '100%';
    
                //imgObjPreview.src = docObj.files[0].getAsDataURL();
    
                //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式
    
                imgObjPreview.src = window.URL.createObjectURL(docObj.files[i]);
    
            }
    
            else {
    
                //IE下，使用滤镜
    
                docObj.select();
    
                var imgSrc = document.selection.createRange().text;
    
                alert(imgSrc)
    
                var localImagId = document.getElementById("img" + i);
    
                //必须设置初始大小
    
                localImagId.style.width = "100%";
    
                localImagId.style.height = "100%";
    
                //图片异常的捕捉，防止用户修改后缀来伪造图片
    
                try {
    
                    localImagId.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale)";
    
                    localImagId.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = imgSrc;
    
                }
    
                catch (e) {
    
                    alert("您上传的图片格式不正确，请重新选择!");
    
                    return false;
    
                }
    
                imgObjPreview.style.display = 'none';
    
                document.selection.empty();
    
    
            }
    
        }  
    
    
    
        return true;
    
    }
    
    
    
     -->
   

   
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
    var i=1;
    var g=1;
   function add(){
    $("#myCarousel").carousel('pause');

   if (i<10) {
  document.getElementById("carousel-indicators").insertAdjacentHTML('beforeEnd','<li id="li_'+i+'" data-target="#myCarousel" data-slide-to="'+i+'" style="margin-bottom: -40px;background-color:#666"></li>');
  document.getElementById("carousel-inner").insertAdjacentHTML('beforeEnd','<div id="div_'+i+'" class="item"><div class="edit-content-form" style="clear:both"> <label class="checkbox check-title" style="text-align:center;margin-top:-5px"><span style="color:red">*</span>商品名称：</label><input type="text" class="name_text div_" value="" style="width:35%;margin-left:0px;margin-top:5px;"><a href="javascript:" id="addgoods"><img src="/static/images/add.png" onclick="add()"></a><a href="javascript:" id=""><img src="/static/images/useddel.png" onclick="del('+i+')"></a><input type="text" class="iddd" id="inp_'+i+'"  style="display:none"></div><div class="edit-content-form" style="clear:both"><label class="checkbox check-title" style="text-align:center;margin-top:-5px"><span style="color:red">*</span>商品价格：</label><input type="text" class="pri price_" onkeyup="math('+i+')" id="price_'+i+'" value="" style="width:10%;margin-left:0px;margin-top:5px;"></div></div>');
   i = i + 1;
   $('#myCarousel').carousel('next')
}
  else{alert("最多只能添加10件商品");}
   
  }
  mi = 1;
     function madd(){
    $("#myCarousel2").carousel('pause');
    if (mi<10) {
  document.getElementById("carousel-indicators2").insertAdjacentHTML('beforeEnd','<li data-target="#myCarousel2" data-slide-to="'+mi+'" id="mli_'+mi+'" style="margin-bottom: -40px;background-color:#666"></li>');
  document.getElementById("carousel-inner2").insertAdjacentHTML('beforeEnd','<div id="mdiv_'+mi+'" class="item"><div class="m-edit-content-form" style="clear:both;"><label class="checkbox check-title" style="font-family:"微软雅黑";font-size:18px;text-align:center;"><span style="color:red">*</span>商品名称：</label><input type="text" class="name_text mdiv_" style="width:50%;margin-left:3px;margin-top:20px;height:30px;" value=""><span id="addtxt"></span><a href="javascript:" id=""><img src="/static/images/add.png" onclick="madd()"></a><a href="javascript:" id=""><img src="/static/images/useddel.png" onclick="mdel('+mi+')"></a><input type="text" class="middd" id="minp_'+mi+'" style="display:none"></div><div class="m-edit-content-form" style="clear:both;"> <label class="checkbox check-title" style="font-family:"微软雅黑";font-size:18px;text-align:center;"><span style="color:red">*</span>商品价格：</label><input type="text" class="pri mprice_" id="mprice_'+mi+'" onkeyup="mmath('+mi+')" style="width:50%;margin-left:3px;margin-top:20px;height:30px;" value=""></div></div>');
   mi = mi + 1;
   $('#myCarousel2').carousel('next');
    $( "#myCarousel2" ).on( "swipeleft", function( e ) {
    $('#myCarousel2').carousel('next')
    } );
    $( "#myCarousel2" ).on( "swiperight", function( e ) {
     $('#myCarousel2').carousel('prev')
    } );
}
else{
  alert("最多只能添加10件商品")
}} 
   
//判断两个单选组被选中的值是否等于空
// if($('#birthday').text())
// if($(":radio[name='r1']:checked").val()==null)
// alert("有题目为空，请补充完整");
// else
// document.location.href="https://123.sogou.com/";
// })
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
    })
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

    $('#qtime').flatpickr({
        enableTime: true
    });
    if(screen.width<768){
     $("#pcxx").remove();

            $("#edui1").css("width","");

    }

    
   
function del(o){
  $('#myCarousel').carousel('prev');
 document.getElementById("carousel-inner").removeChild(document.getElementById("div_"+o));
 document.getElementById("carousel-indicators").removeChild(document.getElementById("li_"+o));
 // $("#inp_"+o).remove();
i=i-1;

}
function mdel(mo){
  $('#myCarousel2').carousel('prev');
 document.getElementById("carousel-inner2").removeChild(document.getElementById("mdiv_"+mo));
 document.getElementById("carousel-indicators2").removeChild(document.getElementById("mli_"+mo));
// $("#minp_"+mo).remove();
mi=mi-1;
}



 $("#push1").click(function(){
 
  var goodsid=[];
  var goodsid1;
  //alert($('#myEditor').val());
 
 if($(".iddd1").length>0){
  goodsid1= $(".iddd1").val();
 }
 else{
  goodsid1=0;
 }
  var shu=[];

  var shu1=[];
  var image=[];
   var goodsname = $("#goodsname").val()
     var goodsprice=$("#price").val();
     var bb;
$(".div_").each(function(i,value){
  //alert($(this).val());
shu.push(value.value);
$(".price_").each(function(j,value1){
shu1.push(value1.value);
$(".iddd").each(function(k,value2){

goodsid.push(value2.value);


  });
});
//alert(goodsid);
if (goodsid[i]=="") {
  goodsid[i]=0;
}
//alert(shu);
bb+="~#~"+shu[i]+"~*~"+shu1[i]+"~*~"+goodsid[i];
//alert(bb);
});

   var aa=goodsname+"~*~"+goodsprice+"~*~"+goodsid1+bb;
aa=aa.replace("undefined","");
// $(".upload_image").each(function(k,value){
 
//  image.push(value.src);
// });
//alert($("#dd li img")[0].src);
 if($('#title').val()==""){
      alert("商品标题是必填项");
      $('#title').focus();
     
     }
     else if($('#title').val().length>20){
      alert("标题过长，请限制在20字以内");
      $('#title').focus();
      
     }
     else if($('#goodsname').val()==""){
      alert("商品名称是必填项");
      $('#goodsname').focus();
       return false;
     }
     else if($('#goodsname').val().length>64){
      alert("商品名称过长，请限制在64字以内");
      $('#goodsname').focus();
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
     // else if($('#id_tags').val()==null){
     //  alert("请选择商品标签");
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
          var goods_detail_str1=aa;
          var district=$('#loc5txt').val();
          var connect_name=$('#connect_name').val();
          var connect_phone=$('#connect_phone').val();
          var connect_wx=$('#connect_wx').val();
          var connect1=$('#myEditor').val();

          var tags=[];

          $('.tags:checked').each(function(){
            tags.push($(this).val());
            

          });
          // for (var i = 0;i<$('input[name="tags"]').length; i++) {
          //   if ($('input[name="tags"]')[i].checked) {
          //     tags.push($('input[name="tags"]')[i].val());
          //   }
            
          // }
          tags.sort();
          $.unique(tags);
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
                data: {'title':title,'goods_detail_str':goods_detail_str1,'tags':tags,'district':district,'connect_name':connect_name,'connect_phone':connect_phone,'connect_wx':connect_wx,'content':connect1,'image':image1,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                beforeSend:function(){
                  $("loading").show();

                },
                complete:function(){
                  $("loading").hide();

                },
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
            });}
         });
     /* else if($('#myEditor').val()==""){
      alert("详细内容是必填项");
     }*/
     
   
   $("#push2").click(function(){
        var mgoodsid=[];
  var mgoodsid1;
  
 
 if($(".iddd1").length>0){
  mgoodsid1= $(".iddd1").val();
 }
 else{
  mgoodsid1=0;
 }
  var mshu=[];

  var mshu1=[];
   var mgoodsname = $("#mgoodsname").val()
     var mgoodsprice=$("#mprice").val();
     var mbb;
$(".mdiv_").each(function(i,value){
  //alert($(this).val());
mshu.push(value.value);
$(".mprice_").each(function(j,value1){
mshu1.push(value1.value);
$(".middd").each(function(k,value2){

mgoodsid.push(value2.value);


  });
});
//alert(goodsid);
if (mgoodsid[i]=="") {
  mgoodsid[i]=0;
}
//alert(shu);
mbb+="~#~"+mshu[i]+"~*~"+mshu1[i]+"~*~"+mgoodsid[i];
//alert(bb);
});

   var goods_detail_str=mgoodsname+"~*~"+mgoodsprice+"~*~"+mgoodsid1+mbb;
goods_detail_str=goods_detail_str.replace("undefined","");
//alert(aa);
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
    //alert(goods_detail_str);
      
     if($('#mtitle').val()==""){

      alert("标题是必填项");
      return false;
     }
     
      else if($('#mbookname').val()==""){

      alert("商品名称是必填项");
      return false;
     }
     else if($('#mprice').val()==""){

      alert("商品价格是必填项");
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
    
    
 else{ var mtitle=$('#mtitle').val();
          var mgoods_detail_str1=goods_detail_str;
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
          var mtags=[];
          $('.mtags:checked').each(function(){
            mtags.push($(this).val());
            //alert(tags);

          });
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
                data: {'title':mtitle,'goods_detail_str':mgoods_detail_str1,'tags':mtags,'district':mdistrict,'connect_name':mconnect_name,'connect_phone':mconnect_phone,'connect_wx':mconnect_wx,'content':mconnect1,'image':mimage1,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
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
            });}
          });
 
    
     $('#id_tags').addClass('form-control');
     $('#id_tags').addClass('selectpicker bla bla bli');
    $('#id_tags').css('width','35%');
    $('#id_tags').css('margin-left','110px');
    $('#id_tags').css('margin-bottom','15px');
    $('#id_tags').css('margin-top','13px');
//     function usedGoodsadd(){
 

// $("#goods_detail_str").val(aa);
//        if($('#title').val()==""){
//       alert("商品标题是必填项");
//       $('#title').focus();
//        return false;
//      }
//      else if($('#title').val().length>20){
//       alert("标题过长，请限制在20字以内");
//       $('#title').focus();
//        return false;
//      }
//      else if($('#goodsname').val()==""){
//       alert("商品名称是必填项");
//       $('#goodsname').focus();
//        return false;
//      }
//      else if($('#goodsname').val().length>64){
//       alert("商品名称过长，请限制在64字以内");
//       $('#goodsname').focus();
//        return false;
//      }
//     else if($('#price').val()==""){
//       alert("商品价格是必填项");
//       $('#price').focus();
//        return false;
//      }
//     else if(!$('#price').val().match(/^(:?(:?\d+))$/)){//(/^(:?(:?\d+.\d+)|(:?\d+))$/))
//        alert('价格请填写整数');
//        $('#price').focus();
//        return false;
//      }
//      // else if($('#id_tags').val()==null){
//      //  alert("请选择商品标签");
//      //   return false;
//      // }
//      else if($(":radio[name='district1']:checked").val()==null){
//       alert("地区是必填项");
//        return false;
//      }
//     else if($(":radio[name='district1']:checked").val()=="OTHER" && $('#loc5txt').val()==""){
//       alert("地区是必填项");
//        return false;
//      }
     
//      else if($('#connect_name').val()==""){
//       alert("联系人是必填项");
//        return false;
//      }
//      else if($('#connect_phone').val()==""){
//       alert("联系电话是必填项");
//        return false;
//      }
//       else if($('#connect_wx').val()==""){
//       alert("微信是必填项");
//       return false;
//      }
//         else{
//           var title=$('#title').val();
//           var goods_detail_str1=aa;
//           var district=$('#loc5txt').val();
//           var connect_name=$('#connect_name').val();
//           var connect_phone=$('#connect_phone').val();
//           var connect_wx=$('#connect_wx').val();
//           var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
//           alert(title);
//           alert(goods_detail_str1);
//           alert(district);
//           alert(connect_name);
//           alert(connect_wx);

          






//         }
//      /* else if($('#myEditor').val()==""){
//       alert("详细内容是必填项");
//      }*/
     
//    }
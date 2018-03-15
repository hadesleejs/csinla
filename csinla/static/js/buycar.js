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
var mimagepu=[];//重新编辑图片解析后的数组手机
          
 for (var i = 0; i < $(".mupload_image").length; i++) {
        //alert($(".upload_image")[i].src);
        var imageUrl = $(".mupload_image")[i].src;
        console.log('imageUrl', imageUrl); 
        convertImgToBase64(imageUrl, function(base64Img){ 
          
        mimagepu.push(base64Img);
        

}); 
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
            '<img id="uploadImage_' + i + '" src="' + e.target.result + '" class="upload_image" />'+ 
             
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
            '<img id="muploadImage_' + i + '" src="' + e.target.result + '" class="mupload_image" />'+ 
             
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

    // function setImagePreviews(avalue) {

    //     var docObj = document.getElementById("avatar-selector1");

    //     var dd3 = document.getElementById("dd3");

    //     dd3.innerHTML = "";

    //     var fileList = docObj.files;

    //     for (var i = 0; i < 9; i++) {            



    //         dd3.innerHTML += "<li style='float:left;margin-top:30px' > <img id='img" + i + "'  /> </li>";

    //         var imgObjPreview = document.getElementById("img"+i); 
    //         if(i<8){
    //         var nu=9-i;
    //         document.getElementById("upnumber").innerHTML="还可以上传"+nu+"张";}
    //         else{
    //           var nu=8-i;
    //         document.getElementById("upnumber").innerHTML="还可以上传"+nu+"张";
    //       }
            
            

    //         if (docObj.files && docObj.files[i]) {

    //             //火狐下，直接设img属性

    //             imgObjPreview.style.display = 'block';

    //             imgObjPreview.style.width = '100%';

    //             imgObjPreview.style.height = '100%';

    //             //imgObjPreview.src = docObj.files[0].getAsDataURL();

    //             //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式

    //             imgObjPreview.src = window.URL.createObjectURL(docObj.files[i]);

    //         }

    //         else {

    //             //IE下，使用滤镜

    //             docObj.select();

    //             var imgSrc = document.selection.createRange().text;

    //             alert(imgSrc)

    //             var localImagId = document.getElementById("img" + i);

    //             //必须设置初始大小

    //             localImagId.style.width = "100%";

    //             localImagId.style.height = "100%";

    //             //图片异常的捕捉，防止用户修改后缀来伪造图片

    //             try {

    //                 localImagId.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale)";

    //                 localImagId.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = imgSrc;

    //             }

    //             catch (e) {

    //                 alert("您上传的图片格式不正确，请重新选择!");

    //                 return false;

    //             }

    //             imgObjPreview.style.display = 'none';

    //             document.selection.empty();


    //         }

    //     }  



    //     return true;

    // }


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
    $('#birthday1').flatpickr({
           minDate:"today",
         enableTime:false,
      //   onClose:function(dateObj,dateStr,instance){
      //   alert($('#birthday').val())
      // }
         maxDate:new Date().fp_incr(90)
        });
    $('#carage').flatpickr({
          
        });
    
});

     var h=$(":radio[name='car_type']:checked").val();
    // $('#othertxt').val(h);
   var k=$(":radio[name='level_type']:checked").val();
    // $('#lv4txt').val(k);
 
     if($('#othertxt').val()!="" && $(":radio[name='car_type']:checked").val()==null){
    $(":radio[name='car_type']").attr("checked","other");
    $('#othertxt').show();
   }
   
    if($('#lv4txt').val()!="" && $(":radio[name='level_type']:checked").val()==null){
    $(":radio[name='level_type']").attr("checked","other");
    $('#lv4txt').show();
   }
  

    if($('#mlv4').val()!="" && $('#mlv option:selected').val()=="select"){
    $('#mlv option:selected').val("OTHER");
    $('#mlv').hide();
    $('#mlv4').show();
   }
   if($('#mleveltxt').val()!="" && $('#mlevel option:selected').val()=="select"){
    $('#mlevel option:selected').val("OTHER");
    $('#mlevel').hide();
    $('#mleveltxt').show();
   }
    $('#qtime').flatpickr({
        enableTime: true
    });
    function ot(){
    if($(":radio[name='level_type']:checked").val()=="other"){
    $('#lv4txt').css('display','inline-block');
  }
  else{
    var level_typ=$(":radio[name='level_type']:checked").val();
   $('#lv4txt').val(level_typ);
   $('#lv4txt').hide();
 
  }
  if($(":radio[name='car_type']:checked").val()=="other"){
    $('#othertxt').css('display','inline-block');
  }
  else{
    var car_typ=$(":radio[name='car_type']:checked").val();
   $('#othertxt').val(car_typ);
   $('#othertxt').hide();
 
  }
   }
      var a= $('#mlv option:selected');
      // $('#mlv4').val(a.val());
     var b=$('#mlevel option:selected');
     // $('#mleveltxt').val(b.val());
    if (a.val()=="其他") {
      $('#mlv4').show();
      $('#mlv').hide();
    }
    if (b.val()=="其他") {
      $('#mleveltxt').show();
      $('#mlevel').hide();
    }
    function selectother(){
     var a= $('#mlv option:selected');
     var b=$('#mlevel option:selected');
    if (a.val()=="其他") {
      $('#mlv4').show();
      $('#mlv').hide();
    }
    else{
      var lv4=a.val();
      $('#mlv4').val(lv4);
      //alert($('#mlv4').val());
    }
    if (b.val()=="其他") {
      $('#mleveltxt').show();
      $('#mlevel').hide();
    }
    else{
      var mleveltx=b.val()
      $('#mleveltxt').val(mleveltx);
    }
    
  }
    
    if ($(":radio[name='car_type']:checked").val()=="other") {
      $('#othertxt').show();
    }
    if ($(":radio[name='level_type']:checked").val()=="other") {
      $('#lv4txt').show();
    }
    $("#push1").click(function(){
     
      if ($('#birthday').val()=="") {
     alert("到期时间是必填项");
     return false;
   }
     else if($('#title').val()==""){
      alert("标题是必填项");
      return false;
     }
     else if($(":radio[name='car_type']:checked").val()==null){
      alert("类别是必填项");
      return false;
     }
     else if($('#brand').val()==""){
      alert("品牌是必填项");
      return false;
     }
     else if($("#carage1").val()==""){
      alert("车龄是必填项");
      //alert($("#carage1").val());
      return false;
     }
     else if($('#vehicle_miles').val()==""){
      alert("里程是必填项");
      return false;
     }
     else if($('#fee').val()==""){
      alert("价格是必填项");
      return false;
     }
     else if($(":radio[name='level_type']:checked").val()==null){
      alert("级别是必填项");
      return false;
     }
     else if($(":radio[name='transmission_type']:checked").val()==null){
      alert("变速器是必填项");
      return false;
     }

     else if($('#displacement').val()==""){
      alert("排量是必填项");
      return false;
     }
     else if($(":radio[name='drive_type']:checked").val()==null){
      alert("驱动是必填项");
      return false;
     }
     else if($('#inside_color').val()==""){
      alert("外部颜色是必填项");
      return false;
     }
     else if($('#outside_color').val()==""){
      alert("内部颜色是必填项");
      return false;
     }
     else if($(":radio[name='oil_type']:checked").val()==null){
      alert("燃油类型是必填项");
      return false;
     }
     else if($(":radio[name='turbo']:checked").val()==null){
      alert("涡轮增压是必填项");
      return false;
     }
     else if($('#vin_number').val()==""){
      alert("Vin number是必填项");
      return false;
     }
     else if($('#contactor').val()==""){
      alert("联系人是必填项");
      return false;
     }
     else if($('#phone').val()==""){
      alert("联系电话是必填项");
      return false;
     }
      else if($('#weixin').val()==""){
      alert("联系微信是必填项");
      return false;
     }
     else if($('#contact_way').val()==""){
      alert("汽车所在地址是必填项");
      return false;
     }
     else{
       var expire_date=$('#birthday').val();
      var car_type=$("#othertxt").val();
      var brand=$('#brand').val();
      var title=$('#title').val();
      var vehicle_age=$("#carage1 option:selected").val();
          var vehicle_miles=$('#vehicle_miles').val();
          // var share=$(":radio[name='share']:checked").val();
          var fee2=$('#fee').val();
          var displacement=$("#displacement").val();
          var inside_color=$('#inside_color').val();
          var outside_color=$('#outside_color').val();
          var vin_number=$('#vin_number').val();
          var oil_type=$(":radio[name='oil_type']:checked").val();
          var turbo=$(":radio[name='turbo']:checked").val();
          var drive_type=$(":radio[name='drive_type']:checked").val();
          var transmission_type=$(":radio[name='transmission_type']:checked").val();
          var level_type=$("#lv4txt").val();
          
          var contact_way=$('#contact_way').val();
          var contactor=$('#contactor').val();
          
          var phone=$('#phone').val();
          var weixin=$('#weixin').val();
          var connect=$("#myEditor").val();
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
        //alert(image1);
    
  $("#push1").attr({"disabled":"disabled"});
  //alert($(".upload_image").length);
  
         $.ajax({
                type: "POST",
                dataType: "json",
                url: "",
                 traditional: true,
                data: {
                  'expire_date':expire_date,
                  'car_type':car_type,
                  'brand':brand,
                  'vehicle_age':vehicle_age,
                  'title':title,
                  'vehicle_miles':vehicle_miles,
                 
                  'fee2':fee2,
                  'displacement':displacement,
                  'inside_color':inside_color,
                  'outside_color':outside_color,
                  'vin_number':vin_number,
                  'oil_type':oil_type,
                     
                  'turbo':turbo,
                  'contact_way':contact_way,
                  'drive_type':drive_type,
                  'transmission_type':transmission_type,
                  'level_type':level_type,
                  
                  'content':connect,
                'contactor':contactor,'phone':phone,'weixin':weixin,'image':image1,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 //
                
               if(data.code==0 && data.post_id>0){
                 // alert(data.post_id);}

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
   })
     $("#push2").click(function(){
      if ($('#birthday1').val()=="") {
     alert("到期时间是必填项");
      return false;}
     else if($('#mtitle').val()==""){
      alert("标题是必填项");
      return false;
     }
      else if ($('#mlv option:selected').val()=="select") {
      alert("类别是必填项");
      return false;
    }
     else if($('#mbrand').val()==""){
      alert("品牌是必填项");
      return false;
     }
      else if($("#carage2").val()==""){
      alert("车龄是必填项");
      alert($("#carage2").val());
      return false;
     }
   
     else if($('#mvehicle_miles').val()==""){
      alert("里程是必填项");
      return false;
     }
     else if($('#mfee').val()==""){
      alert("价格是必填项");
      return false;
     }
     else if ($('#mlevel option:selected').val()=="select") {
      alert("级别是必填项");
      return false;
    }
    else if ($('#mtransmission_type option:selected').val()=="select") {
      alert("变速器是必填项");
      return false;
    }
     else if($('#mdisplacement').val()==""){
      alert("排量是必填项");
      return false;
     }
     else if ($('#mdrive_type option:selected').val()=="select") {
      alert("驱动是必填项");
      return false;
    }
     else if($('#minside_color').val()==""){
      alert("外部颜色是必填项");
      return false;
     }
     else if($('#moutside_color').val()==""){
      alert("内部颜色是必填项");
      return false;
     }
     else if ($('#moil_type option:selected').val()=="select") {
      alert("燃油类型是必填项");
      return false;
    }
    else if ($('#mturbo option:selected').val()=="select") {
      alert("涡轮增压是必填项");
      return false;
    }
     else if($('#mvin_number').val()==""){
      alert("Vin number是必填项");
      return false;
     }
     else if($('#mcontactor').val()==""){
      alert("联系人是必填项");
      return false;
     }
     else if($('#mphone').val()==""){
      alert("联系电话是必填项");
      return false;
     }
      else if($('#mweixin').val()==""){
      alert("联系微信是必填项");
      return false;
     }
     else if($('#mcontact_way').val()==""){
      alert("汽车所在地址是必填项");
      return false;
     }
     else{

       var mexpire_date=$('#birthday1').val();
      var mcar_type=$('#mlv4').val();
      var mbrand=$('#mbrand').val();
      var mtitle=$('#mtitle').val();
      var mvehicle_age=$("#carage2 option:selected").val();
          var mvehicle_miles=$('#mvehicle_miles').val();
          // var mshare=$('#mshare option:selected').val();
          var mfee2=$('#mfee').val();
          var mdisplacement=$("#mdisplacement").val();
          var minside_color=$('#minside_color').val();
          var moutside_color=$('#moutside_color').val();
          var mvin_number=$('#mvin_number').val();
          var moil_type=$('#moil_type option:selected').val();
          var mturbo=$("#mturbo option:selected").val();
          var mdrive_type=$("#mdrive_type option:selected").val();
          var mtransmission_type=$("#mtransmission_type option:selected").val();
          var mlevel_type=$("#mleveltxt").val();
          
          var mcontact_way=$('#mcontact_way').val();
          var mcontactor=$('#mcontactor').val();
          
          var mphone=$('#mphone').val();
          var mweixin=$('#mweixin').val();
          var mconnect=$("#mmyEditor").val();
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
  
  //alert($(".upload_image").length);
  
         $.ajax({
                type: "POST",
                dataType: "json",
                url: "",
                 traditional: true,
                data: {
                  'expire_date':mexpire_date,
                  'car_type':mcar_type,
                  'brand':mbrand,
                  'vehicle_age':mvehicle_age,
                  'title':mtitle,
                  'vehicle_miles':mvehicle_miles,
              
                  'fee2':mfee2,
                  'displacement':mdisplacement,
                  'inside_color':minside_color,
                  'outside_color':moutside_color,
                  'vin_number':mvin_number,
                  'oil_type':moil_type,
                     
                  'turbo':mturbo,
                  'contact_way':mcontact_way,
                  'drive_type':mdrive_type,
                  'transmission_type':mtransmission_type,
                  'level_type':mlevel_type,
                  
                  'content':mconnect,
                'contactor':mcontactor,'phone':mphone,'weixin':mweixin,'image':mimage1,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
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
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
     var b=$('#mhouse option:selected');
     var c=$('#mrent option:selected');
    if (a.val()=="OTHER") {
      $('#mlocaltxt').show();
      $('#mlocal').hide();
    }
    else{
      var mloc=a.val();
      $('#mlocaltxt').val(mloc);    }
    
  
    if (b.val()=="other") {
      $('#mhousetxt').show();
      $('#mhouse').hide();
    }
      else{
      var mhousetx=b.val();
      $('#mhousetxt').val(mhousetx);    }
    
  
    if (c.val()=="other") {
      $('#mrenttxt').show();
      $('#mrent').hide();
    }
      else{
      var mrent1=c.val();
      $('#mrenttxt').val(mrent1);    }
    
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
   
    var funAppendImage = function() {
      file = files[i];
      if (file&&i<9) {
        var reader = new FileReader()
        reader.onload = function(e) {
           
             html =html + '<li id="uploadList_'+ i +'" class="upload_append_list">'+ 
            '<a href="javascript:" class="upload_delete" title="删除" data-index="'+ i +'"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +
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
    $("#uploadList_" + file.index).remove();
    
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
            '<a href="javascript:" class="mupload_delete" title="删除" data-index="'+ i +'"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +
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
    $("#muploadList_" + file.index).remove();
   
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
// function mdelimage(mimagenum){
//   $("#muploadList_"+mimagenum).remove();
// }
// function delimage(imagenum){
//   $("#uploadList_"+imagenum).remove();
// }

//上传图片选择文件改变后刷新预览图
// $("#avatar-selector").change(function(e){
//     //获取目标文件
//     var file = e.target.files||e.dataTransfer.files;
//     //如果目标文件存在
//     if(file){
//         //定义一个文件阅读器
//         var reader = new FileReader();
//         //文件装载后将其显示在图片预览里
//         reader.onload=function(){
//             $("#img_preview").attr("src", this.result);
//         }
//         //装载文件
//         reader.readAsDataURL(file[0]);
//     }
// });


    //下面用于多图片上传预览功能

    // function setImagePreviews(avalue) {

    //     var docObj = document.getElementById("avatar-selector1");

    //     var dd3 = document.getElementById("dd3");

    //     dd3.innerHTML = "";

    //     var fileList = docObj.files;

    //     for (var i = 0; i < 10; i++) {            

    //       if(i<9){

    //         dd3.innerHTML += "<li style='float:left;margin-top:30px' > <img id='img" + i + "'  /> </li>";

    //         var imgObjPreview = document.getElementById("img"+i); 
    //         if(i<8){
    //         var nu=9-i;
    //         document.getElementById("upnumber").innerHTML="还可以上传"+nu+"张";}
    //         else{
    //           var nu=8-i;
    //         document.getElementById("upnumber").innerHTML="还可以上传"+nu+"张";
          
    //         }}
    //         else{alert('只能上传9张');}
            

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




   function showinput(){
  if($(":radio[name='district']:checked").val()=="OTHER"){
    $('#loc5txt').css('display','inline-block');
  }
  else{
    var distri=$(":radio[name='district']:checked").val();
    $('#loc5txt').hide();
   $('#loc5txt').val(distri);
 
  }

   if($(":radio[name='house_type']:checked").val()=="other"){
     $('#house5txt').css('display','inline-block');
     }
     else{
       $('#house5txt').hide();
       var house_typ=$(":radio[name='house_type']:checked").val();
       $('#house5txt').val(house_typ);
     }
    if($(":radio[name='room_type']:checked").val()=="other"){
      $('#rent4txt').css('display','inline-block');
     }
     else{
      $('#rent4txt').hide();
       var room_typ=$(":radio[name='room_type']:checked").val();
   $('#rent4txt').val(room_typ);
     }
}
// thisURL = document.URL; 
// thisHREF = document.location.href; 
// thisSLoc = self.location.href; 
// thisDLoc = document.location; 
// strwrite = thisURL ;

// document.write( strwrite ); 
// document.write(strwrite.substring(str.length-1,3))
  
   
//判断两个单选组被选中的值是否等于空
// if($('#birthday').text())
// if($(":radio[name='r1']:checked").val()==null)
// alert("有题目为空，请补充完整");
// else
// document.location.href="https://123.sogou.com/";
// })
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
     if($('#loc5txt').val()!="" && $(":radio[name='district']:checked").val()==null){
    $(":radio[name='district']").attr("checked","OTHER");
    $('#loc5txt').show();
   }
    if($('#mlocaltxt').val()!="" && $('#mlocal option:selected').val()=="select"){
    $('#mlocal option:selected').val("OTHER");
    $('#mlocal').hide();
    $('#mlocaltxt').show();
   }
   if($('#house5txt').val()!="" && $(":radio[name='house_type']:checked").val()==null){
    $(":radio[name='house_type']").attr("checked","other");
    $('#house5txt').show();
   }
    if($('#mhousetxt').val()!="" && $('#mhouse option:selected').val()=="select"){
    $('#mhouse option:selected').val("other");
    $('#mhouse').hide();
    $('#mhousetxt').show();
   }
   if($('#rent4txt').val()!="" && $(":radio[name='room_type']:checked").val()==null){
    $(":radio[name='room_type']").attr("checked","other");
    $('#rent4txt').show();
   }
    if($('#mrenttxt').val()!="" && $('#mrent option:selected').val()=="select"){
    $('#mrent option:selected').val("other");
    $('#mrent').hide();
    $('#mrenttxt').show();
   }
});

   
     $("#push1").click(function(){
      if ($('#birthday').val()=="") {
     alert("到期时间是必填项");
     return false;
   }
     else if($('#title').val()==""){
      alert("帖子标题是必填项");
      return false;
     }
     else if($('#birthday5').val()=="" || $('#birthday6').val()==""){
      alert("租期是必填项");
      return false;
     }
     else if($(":radio[name='district']:checked").val()==null){
      alert("地区是必填项");
      return false;
     }
     else if($(":radio[name='share']:checked").val()==null){
      alert("方式是必填项");
      return false;
     }
     else if($('#fee').val()==""){
      alert("月租是必填项");
      return false;
     }
     else if($(":radio[name='house_type']:checked").val()==null){
      alert("整套房型是必填项");
      return false;
     }
     else if($(":radio[name='room_type']:checked").val()==null){
      alert("出租其中是必填项");
      return false;
     }
     else if($(":radio[name='pet']:checked").val()==null){
      alert("宠物是必填项");
      return false;
     }
     else if($(":radio[name='smoke']:checked").val()==null){
      alert("抽烟是必填项");
      return false;
     }
     else if($(":radio[name='parking']:checked").val()==null){
      alert("停车位是必填项");
      return false;
     }
     else if($(":radio[name='gender_require']:checked").val()==null){
      alert("性别要求是必填项");
      return false;
     }
      else if($('#alladdress').val()==""){
      alert("具体地址是必填项");
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
      alert("微信是必填项");
      return false;
     }
     else{
      var expire_date=$('#birthday').val();
      var rent_begins=$('#birthday5').val();
      var rent_ends=$('#birthday6').val();
      var title=$('#title').val();
      var type=$(":radio[name='type']:checked").val() 
          var district=$('#loc5txt').val();
          var share=$(":radio[name='share']:checked").val();
          var fee=$('#fee').val();
          var house_type=$("#house5txt").val();
          var room_type=$('#rent4txt').val();
          var pet=$(":radio[name='pet']:checked").val();
          var smoke=$(":radio[name='smoke']:checked").val();
          var parking=$(":radio[name='parking']:checked").val();
          var driving_time_toschool_hour=$("#hour_start_select1 option:selected").val();
          var driving_time_toschool_minute=$("#hour_end_select1 option:selected").val();
          var transit_time_toschool_hour=$("#hour_start_select option:selected").val();
          var transit_time_toschool_minute=$("#hour_end_select option:selected").val();
          var gender_require=$(":radio[name='gender_require']:checked").val();
          var address=$('#alladdress').val();
          var contactor=$('#contactor').val()
          
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
 
        //alert(image1);
         $.ajax({
                type: "POST",
                dataType: "json",
                url: "",
                traditional: true,
                data: {
                  'expire_date':expire_date,
                  'rent_begins':rent_begins,
                  'rent_ends':rent_ends,
                  'type':type,
                  'title':title,
                  'share':share,
                  'district':district,
                  'fee':fee,
                  'house_type':house_type,
                  'room_type':room_type,
                  'pet':pet,
                  'gender_require':gender_require,
                  'smoke':smoke,
                  'parking':parking,
                  'address':address,
                  'driving_time_toschool_hour':driving_time_toschool_hour,
                  'transit_time_toschool_hour':transit_time_toschool_hour,
                  'driving_time_toschool_minute':driving_time_toschool_minute,
                  'transit_time_toschool_minute':transit_time_toschool_minute,
                  'content':connect,
                'contactor':contactor,'phone':phone,'weixin':weixin,'image':image1,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
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
  $("#push2").click(function(){
      if ($('#birthday4').val()=="") {
     alert("到期时间是必填项");
     return false;

   }
     else if($('#mtitle').val()==""){
      alert("帖子标题是必填项");
      return false;
     }
     else if($('#birthday7').val()==""){
      alert("起始日期是必填项");
      return false;
     }
     else if($('#birthday8').val()==""){
      alert("终止日期是必填项");
      return false;
     }
     else if ($('#mlocal option:selected').val()=="select") {
      alert("地区是必填项");
      return false;
     }
     else if ($('#mshare option:selected').val()=="select") {
      alert("方式是必填项");
      return false;
     }
     else if($('#mfee').val()==""){
      alert("月租是必填项");
      return false;
     }
     else if ($('#mhouse option:selected').val()=="select") {
      alert("整套房型是必填项");
      return false;
     }
     else if ($('#mrent option:selected').val()=="select") {
      alert("出租其中是必填项");
      return false;
     }
     else if ($('#mpet option:selected').val()=="select") {
      alert("宠物是必填项");
      return false;
     }
     else if ($('#msmoke option:selected').val()=="select") {
      alert("抽烟是必填项");
      return false;
     }
     else if ($('#mparking option:selected').val()=="select") {
      alert("车位是必填项");
      return false;
     }
      else if ($('#mgender_require option:selected').val()=="select") {
      alert("性别要求是必填项");
      return false;
     }
      else if($('#malladdress').val()==""){
      alert("地址是必填项");
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
      alert("微信是必填项");
      return false;
     }
     else if($('#mweixin').val()==""){
      alert("微信是必填项");
      return false;
     }
     else{
    var mexpire_date=$('#birthday4').val();
      var mrent_begins=$('#birthday7').val();
      var mrent_ends=$('#birthday8').val();
      var mtitle=$('#mtitle').val();
      var mtype=$('#mtype option:selected').val();
          var mdistrict=$('#mlocaltxt').val();
          var mshare=$('#mshare option:selected').val();
          var mfee=$('#mfee').val();
          var mhouse_type=$("#mhousetxt").val();
          var mroom_type=$('#mrenttxt').val();
          var mpet=$('#mpet option:selected').val();
          var msmoke=$('#msmoke option:selected').val();
          var mparking=$('#mparking option:selected').val();
          var mdriving_time_toschool_hour=$("#mhour_start_select1 option:selected").val();
          var mdriving_time_toschool_minute=$("#mhour_end_select1 option:selected").val();
          var mtransit_time_toschool_hour=$("#mhour_start_select option:selected").val();
          var mtransit_time_toschool_minute=$("#mhour_end_select option:selected").val();
          var mgender_require=$('#mgender_require option:selected').val();
          var maddress=$('#malladdress').val();
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
        //alert(image1);
     $("#push2").attr({"disabled":"disabled"});
  

         $.ajax({
                type: "POST",
                dataType: "json",
                url: "",
                 traditional: true,
                data: {
                  'expire_date':mexpire_date,
                  'rent_begins':mrent_begins,
                  'rent_ends':mrent_ends,
                  'type':mtype,
                  'title':mtitle,
                  'share':mshare,
                  'district':mdistrict,
                  'fee':mfee,
                  'house_type':mhouse_type,
                  'room_type':mroom_type,
                  'pet':mpet,
                  'gender_require':mgender_require,
                  'smoke':msmoke,
                  'parking':mparking,
                  'address':maddress,
                  'driving_time_toschool_hour':mdriving_time_toschool_hour,
                  'transit_time_toschool_hour':mtransit_time_toschool_hour,
                  'driving_time_toschool_minute':mdriving_time_toschool_minute,
                  'transit_time_toschool_minute':mtransit_time_toschool_minute,
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
function gotoentire(){
      window.location.href='/posts/add/entire_rent/';
    }
    function mgotoentire(){
  if($("#mtype").val()=='整套出租'){
  window.location.href='/posts/add/entire_rent/';}
}
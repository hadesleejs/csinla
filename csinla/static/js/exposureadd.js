var hh=$("#dd").html();
// function convertImgToBase64(url, callback, outputFormat){ 
// var canvas = document.createElement('CANVAS'); 
// var ctx = canvas.getContext('2d'); 
// var img = new Image; 
// img.crossOrigin = 'Anonymous'; 
// img.onload = function(){ 
// canvas.height = 300; 
// canvas.width = 300; 
// ctx.drawImage(img,0,0,300, 300); 
// var dataURL = canvas.toDataURL('image/png'); 
// callback.call(this, dataURL); 
// // Clean up 
// canvas = null; 
// }; 
// img.src = url; 
// } 
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
        $("#dd").html(html);
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
        $("#dd3").html(html1);
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
 $('.upload_delete').click(function(){
     $(this).parent("li.upload_append_list").remove();
   });
  $('.mupload_delete').click(function(){
     $(this).parent("li.mupload_append_list").remove();
   });

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

   
    $('#id_tags').addClass('form-control');
    $('#id_tags').css('width','35%');
    $('#id_tags').css('margin-left','105px');
    $('#id_tags').css('margin-bottom','17px');
    $("#push1").click(function(){
      var title=$("#title").val();
      var connect1=$("#myEditor").val();
      //alert($(".upload_image").length);
      var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
         
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
        //alert(image1);
         $.ajax({
                type: "POST",
                dataType: "json",
                url: "",
                 traditional: true,
                data: {'title':title,'content':connect1,'image':image1,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
                success: function (data) {
                // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
                 // alert(data.post_id);
                
                if(data.code==0 && data.post_id>0){
                 window.location.href="/posts/complete/"+data.post_id+"";      
                           }
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

    })
    $("#push2").click(function(){
      var mtitle=$("#mtitle").val();
      var mconnect1=$("#mmyEditor").val();
      //alert($(".mupload_image").length);
      var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
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
          
         $.ajax({
                type: "POST",
                dataType: "json",
                url: "",
                 traditional: true,
                data: {'title':mtitle,'content':mconnect1,'image':mimage1,'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
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

    })




var params = {
  fileInput: $("#avatar-selector").get(0),
  //dragDrop: $("#fileDragArea").get(0),
 upButton: $("#fileSubmit").get(0),
  //url: $("#uploadForm").attr("action"),
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
            '<a href="javascript:" class="upload_delete" title="删除" data-index="'+ i +'"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +
            '<img id="uploadImage_' + i + '" src="' + e.target.result + '" class="upload_image" />'+ 
             
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




   
thisURL = document.URL; 
thisHREF = document.location.href; 
thisSLoc = self.location.href; 
thisDLoc = document.location; 
strwrite = thisURL ;

document.write( strwrite ); 
document.write(strwrite.substring(str.length-1,3))
    
   
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
});

    
     i = 1;
     function add(){
    if (i<5) {
  document.getElementById("addtxt").innerHTML+='<input name="text" id="div_'+i+'" name="text_'+i+'" type="text" value="" style="width:10%;margin-left:10px;"  /><input type="button" id="dele_'+i+'" value="删除"  onclick="del('+i+')"/>';
  document.getElementById("addprice").innerHTML+='<input name="text" id="price_'+i+'" name="text_'+i+'" type="text" value="" style="width:10%;margin-left:10px;"  />';
  i = i + 1;
}
else{
  alert("最多只能添加5件商品")
}}
function del(o){
 document.getElementById("addtxt").removeChild(document.getElementById("div_"+o));
 document.getElementById("addtxt").removeChild(document.getElementById("dele_"+o));
 document.getElementById("addprice").removeChild(document.getElementById("price_"+o));
}

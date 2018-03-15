var params = {

  fileInput: $("#file1").get(0),

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



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html ='<li id="uploadList_1" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage(1)" data-index="1"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_1" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          i++;

          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd").html(html);
        $("#label_file1").hide();
        $("#file1").hide();
        $("#label_file2").show();
        $("#file2").show();


      

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

var params1 = {

  fileInput: $("#file2").get(0),

  //dragDrop: $("#fileDragArea").get(0),

   upButton: $("#titi").get(0),

   

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

     i = 0;

    var html1 ='';

    var funAppendImage = function() {

      file = files[i];
      



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html1 = $("#dd").html() +'<li id="uploadList_2" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage1(2)" data-index="2"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_2" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          
       i++;
          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd").html(html1);
        $("#label_file1").hide();
        $("#file1").hide();
        $("#label_file2").hide();
        $("#file2").hide();


      

        if (html1) {

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

ZXXFILE1 = $.extend(ZXXFILE1, params1);

ZXXFILE1.init();
function delimage(imagenum){
    $("#label_file"+imagenum).show();
     $("#file"+imagenum).show();
     $("#label_file"+(imagenum+1)).hide();
     $("#file"+(imagenum+1)).hide();
     $("#uploadList_"+imagenum).remove();
   


}

function delimage1(imagenum1){

     $("#uploadList_"+imagenum1).remove();
     $("#label_file"+imagenum1).show();
     $("#file"+imagenum1).show();


}



var params2 = {

  fileInput: $("#file7").get(0),

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

    var html2 = '', i = 0;

    $("#dd1").html('<div class="upload_loading"></div>');

    var funAppendImage = function() {

      file = files[i];



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html2 ='<li id="uploadList_7" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage(7)" data-index="7"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_7" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          i++;

          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd1").html(html2);
        $("#label_file7").hide();
        $("#file7").hide();
        $("#label_file8").show();
        $("#file8").show();


      

        if (html2) {

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

ZXXFILE2 = $.extend(ZXXFILE2, params2);

ZXXFILE2.init();








 

  



//上传图片选择文件改变后刷新预览图

var params3 = {

  fileInput: $("#file8").get(0),

  //dragDrop: $("#fileDragArea").get(0),

   upButton: $("#titi").get(0),

   

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

     i = 0;

    var html3 ='';

    var funAppendImage = function() {

      file = files[i];
      



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html3 = $("#dd1").html() +'<li id="uploadList_8" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage1(8)" data-index="8"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_8" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          
       i++;
          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd1").html(html3);
        $("#label_file7").hide();
        $("#file7").hide();
        $("#label_file8").hide();
        $("#file8").hide();


      

        if (html3) {

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

ZXXFILE3 = $.extend(ZXXFILE3, params3);

ZXXFILE3.init();







var params4 = {

  fileInput: $("#file5").get(0),

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

    var html4 = '', i = 0;

    $("#dd2").html('<div class="upload_loading"></div>');

    var funAppendImage = function() {

      file = files[i];



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html4 ='<li id="uploadList_5" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage(5)" data-index="5"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_5" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          i++;

          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd2").html(html4);
        $("#label_file5").hide();
        $("#file5").hide();
        $("#label_file6").show();
        $("#file6").show();


      

        if (html4) {

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

ZXXFILE4 = $.extend(ZXXFILE4, params4);

ZXXFILE4.init();








 

  



//上传图片选择文件改变后刷新预览图

var params5 = {

  fileInput: $("#file6").get(0),

  //dragDrop: $("#fileDragArea").get(0),

   upButton: $("#titi").get(0),

   

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

     i = 0;

    var html5 ='';

    var funAppendImage = function() {

      file = files[i];
      



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html5 = $("#dd2").html() +'<li id="uploadList_6" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage1(6)" data-index="6"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_6" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          
       i++;
          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd2").html(html5);
        $("#label_file5").hide();
        $("#file5").hide();
        $("#label_file6").hide();
        $("#file6").hide();


      

        if (html5) {

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

ZXXFILE5 = $.extend(ZXXFILE5, params5);

ZXXFILE5.init();



var params6 = {

  fileInput: $("#file3").get(0),

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

    var html6 = '', i = 0;

    $("#dd3").html('<div class="upload_loading"></div>');

    var funAppendImage = function() {

      file = files[i];



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html6 ='<li id="uploadList_3" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage(3)" data-index="3"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_3" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          i++;

          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd3").html(html6);
        $("#label_file3").hide();
        $("#file3").hide();
        $("#label_file4").show();
        $("#file4").show();


      

        if (html6) {

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

ZXXFILE6 = $.extend(ZXXFILE6, params6);

ZXXFILE6.init();








 

  



//上传图片选择文件改变后刷新预览图

var params7 = {

  fileInput: $("#file4").get(0),

  //dragDrop: $("#fileDragArea").get(0),

   upButton: $("#titi").get(0),

   

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

     i = 0;

    var html7 ='';

    var funAppendImage = function() {

      file = files[i];
      



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html7 = $("#dd3").html() +'<li id="uploadList_4" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage1(4)" data-index="4"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_4" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          
       i++;
          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd3").html(html7);
        $("#label_file3").hide();
        $("#file3").hide();
        $("#label_file4").hide();
        $("#file4").hide();


      

        if (html7) {

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

ZXXFILE7 = $.extend(ZXXFILE7, params7);

ZXXFILE7.init();

var params8 = {

  fileInput: $("#file9").get(0),

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

    var html8 = '', i = 0;

    $("#dd8").html('<div class="upload_loading"></div>');

    var funAppendImage = function() {

      file = files[i];



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html8 ='<li id="uploadList_9" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage(9)" data-index="9"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_9" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          i++;

          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd8").html(html8);
        $("#label_file9").hide();
        $("#file9").hide();
        $("#label_file10").show();
        $("#file10").show();


      

        if (html8) {

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

ZXXFILE8 = $.extend(ZXXFILE8, params8);

ZXXFILE8.init();








 

  



//上传图片选择文件改变后刷新预览图

var params9 = {

  fileInput: $("#file10").get(0),

  //dragDrop: $("#fileDragArea").get(0),

   upButton: $("#titi").get(0),

   

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

     i = 0;

    var html9 ='';

    var funAppendImage = function() {

      file = files[i];
      



      if (file) {

        var reader = new FileReader()

        reader.onload = function(e) {

          html9 = $("#dd8").html() +'<li id="uploadList_10" class="upload_append_list">'+ 

            '<a href="javascript:" class="upload_delete" title="删除"  onclick="delimage1(10)" data-index="10"><img src="/static/images/imgdele.png" style="height:16px"></a><br />' +

            '<img id="uploadImage_10" src="' + e.target.result + '" class="upload_image" style="width:auto;height:auto;max-width:100%;max-height:100%;"/>'+ 

             

          '</li>';

         

          
       i++;
          funAppendImage();





        }

       

        reader.readAsDataURL(file);

      } else {

        $("#dd8").html(html9);
        $("#label_file9").hide();
        $("#file9").hide();
        $("#label_file10").hide();
        $("#file10").hide();


      

        if (html9) {

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

ZXXFILE9 = $.extend(ZXXFILE9, params9);

ZXXFILE9.init();
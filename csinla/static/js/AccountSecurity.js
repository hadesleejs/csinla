 var filterInt = function (value) {
      if(/^(\-|\+)?([0-9]+|Infinity)$/.test(value))
        return Number(value);
      return NaN;
    }
    $(function($) {
        // 时间控件初始化
        $('#birthday').flatpickr({
          
        });
        $('#birthday1').flatpickr({
          
        });
        $('#birthday3').flatpickr({
          
        });});

        // 头像裁剪插件初始化
       
     
    
    //     // 评分控件初试化
    //     var myChart = echarts.init(document.getElementById('safety-chart'));
    //     var score = filterInt($('#safety-chart').data('value'));
    //     if (isNaN(score)) {
    //         return;
    //     }
    //     var dataStyle = { 
    //         normal: {
    //             label: {show:false},
    //             labelLine: {show:false}
    //         }
    //     };
    //     var placeHolderStyle = {
    //         normal : {
    //             color: 'rgba(0,0,0,0)',
    //             label: {show:false},
    //             labelLine: {show:false}
    //         },
    //         emphasis : {
    //             color: 'rgba(0,0,0,0)'
    //         }
    //     };
    //     var option = {
    //         title: {
    //             text: score + '%',
    //             x: 'center',
    //             y: 'center',
    //             textStyle: {
    //               color: '#999',
    //               fontSize: 22
    //             }
    //         },
    //         color: ['#85b6b2', '#6d4f8d','#cd5e7e', '#e38980','#f7db88'],
    //         tooltip : {
    //             show: false
    //         },
    //         toolbox: {
    //             show : false,
    //             feature : {
    //                 mark : {show: true},
    //                 dataView : {show: true, readOnly: false},
    //                 restore : {show: true},
    //                 saveAsImage : {show: true}
    //             }
    //         },
    //         series : [
    //             {
    //                 name:'Line 1',
    //                 type:'pie',
    //                 clockWise:false,
    //                 radius : [50,55],
    //                 itemStyle : dataStyle,
    //                 hoverAnimation: false,
    //                 startAngle :90,
    //                 data:[
    //                     {
    //                         value:score,
    //                         name:'01',
    //                         itemStyle:{
    //                             normal:{
    //                                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
    //                                     offset: 0,
    //                                     color: '#e6ed5f'
    //                                 }, {
    //                                     offset: 1,
    //                                     color: '#5ddcb3'
    //                                 }])
    //                             }
    //                         }
    //                     },
    //                     {
    //                         value:100-score,
    //                         name:'01',
    //                         itemStyle:placeHolderStyle
    //                     },
    //                 ]
    //             }

    //         ]
    //     };
    //     myChart.setOption(option);
    // });-->
   


//    $("#save").click(function(){
  

//   //取消
//   $("#image_cancel").click(function() {
//     //清空上传文件的值
//     $(_pageId + inputFileId).val('');
//   });

//  if($(":radio[name='gender']:checked").val()==null){
//       alert("性别是必填项");
//        return false;
//      }
//   else{
//     var username=$("#username").val();
//     var school=$("#school").val();
//     var student_id=$("#studentID").val();
//     var gender=$(":radio[name='gender']:checked").val()
//     var weixin=$("#weixin").val();
//     var phone=$("#phone").val();
//     if (document.getElementById("metadata1").checked==false) {
//          var is_weixin="";}
//     else{
      
//       var is_weixin=$('#metadata1').val();
//     }
//     if (document.getElementById("metadata2").checked==false) {
//          var is_phone="";}
//     else{
      
//       var is_phone=$('#metadata2').val();
//     }
//     if (document.getElementById("metadata3").checked==false) {
//          var is_name="";}
//     else{
      
//       var is_name=$('#metadata3').val();
//     }

        
    
// 　　
//     var image=$("#avatar_preview img")[0].src;
//     if (new RegExp('http:').test(image)) {
//       image="";
//     }    
//     else{
//     var image=$("#avatar_preview img")[0].src;  }
//     var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

//   $.ajax({
//                 type: "POST",
//                 dataType: "json",
//                 url: "",
//                  traditional: true,
//                 data: {
//                   'username':username,
//                   'school':school,
//                   'student_id':student_id,
//                   'gender':gender,
//                   'weixin':weixin,
//                   'phone':phone,
//                   'is_weixin':is_weixin,
//                   'is_phone':is_phone,
//                   'is_name':is_name,
                 
//                   'image':image,
//                   'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
//                 success: function (data) {
//                 // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
//                  //
                
//                 alert(data.msg);
//                 window.location.reload();
  
//                 },
//                 error: function (err) {
//                     alert("err:" + err);
                    
//                 }
//             });
// }
// });
// $("#save1").click(function(){
//  if($(":radio[name='gender1']:checked").val()==null){
//       alert("性别是必填项");
//        return false;
//      }
//   else{
//   var username=$("#username1").val();
//     var school=$("#school1").val();
//     var student_id=$("#studentID1").val();
//     var gender=$(":radio[name='gender1']:checked").val()
//     var weixin=$("#weixin1").val();
//     var phone=$("#phone1").val();
//     if (document.getElementById("metadata4").checked==false) {
//          var is_weixin="";}
//     else{
      
//       var is_weixin=$('#metadata4').val();
//     }
//     if (document.getElementById("metadata5").checked==false) {
//          var is_phone="";}
//     else{
      
//       var is_phone=$('#metadata5').val();
//     }
//     if (document.getElementById("metadata6").checked==false) {
//          var is_name="";}
//     else{
      
//       var is_name=$('#metadata6').val();
//     }

        
    
// 　　
//     var image=$("#avatar_preview1 img")[0].src;
//     if (new RegExp('http:').test(image)) {
//       image="";
//     }    
//     else{
//     var image=$("#avatar_preview1 img")[0].src;  }
//     var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

//   $.ajax({
//                 type: "POST",
//                 dataType: "json",
//                 url: "",
//                  traditional: true,
//                 data: {
//                   'username':username,
//                   'school':school,
//                   'student_id':student_id,
//                   'gender':gender,
//                   'weixin':weixin,
//                   'phone':phone,
//                   'is_weixin':is_weixin,
//                   'is_phone':is_phone,
//                   'is_name':is_name,
                 
//                   'image':image,
//                   'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
//                 success: function (data) {
//                 // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
//                  //
                
//                 alert(data.msg);
//                 window.location.reload();
  
//                 },
//                 error: function (err) {
//                     alert("err:" + err);
                    
//                 }
//             });
  
// }
// });
// $("#save2").click(function(){
//  if($(":radio[name='gender2']:checked").val()==null){
//       alert("性别是必填项");
//        return false;
//      }
//   else{
//   var username=$("#username2").val();
//     var school=$("#school2").val();
//     var student_id=$("#studentID2").val();
//     var gender=$(":radio[name='gender2']:checked").val()
//     var weixin=$("#weixin2").val();
//     var phone=$("#phone2").val();
//     if (document.getElementById("metadata7").checked==false) {
//          var is_weixin="";}
//     else{
      
//       var is_weixin=$('#metadata7').val();
//     }
//     if (document.getElementById("metadata8").checked==false) {
//          var is_phone="";}
//     else{
      
//       var is_phone=$('#metadata8').val();
//     }
//     if (document.getElementById("metadata9").checked==false) {
//          var is_name="";}
//     else{
      
//       var is_name=$('#metadata9').val();
//     }

        
    
// 　　
//     var image=$("#avatar_preview2 img")[0].src;
//     if (new RegExp('http:').test(image)) {
//       image="";
//     }    
//     else{
//     var image=$("#avatar_preview2 img")[0].src;  }
//     var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

//   $.ajax({
//                 type: "POST",
//                 dataType: "json",
//                 url: "",
//                  traditional: true,
//                 data: {
//                   'username':username,
//                   'school':school,
//                   'student_id':student_id,
//                   'gender':gender,
//                   'weixin':weixin,
//                   'phone':phone,
//                   'is_weixin':is_weixin,
//                   'is_phone':is_phone,
//                   'is_name':is_name,
                 
//                   'image':image,
//                   'csrfmiddlewaretoken':csrfmiddlewaretoken},
                
//                 success: function (data) {
//                 // var result = eval("(" + data.d + ")");//这句话是将json语句对象化
//                  //
                
//                 alert(data.msg);
//                 window.location.reload();
  
//                 },
//                 error: function (err) {
//                     alert("err:" + err);
                    
//                 }
//             });
  
// }
// });
/**
 * cropper图片上传
 */
$(function() {
  console.log('cropper图片上传。。。');

  //触发input file
  $('#upload_btn').click(function() {
    console.log('模拟点击。。。');
    $('#btn1').trigger('click');
  });

  //图片上传
  var $image = $('.upload-img > img');
  $image.cropper({
      viewMode: 1,
//      preview: '.img-preview', //不同尺寸预览区
      //aspectRatio: 1, //裁剪比例，NaN-自由选择区域
      autoCropArea: 0.7, //初始裁剪区域占图片比例
      dragMode: 'move',
      aspectRatio: 1 / 1,
      preview: '#avatar_preview',
      movable: false,
      zoomable: false,
      minCropBoxWidth: 100,
      minCropBoxHeight: 100,  
      minContainerWidth: 100,
      minContainerHeight: 100, 
      minCanvasWidth: 100,
      minCanvasHeight: 100,  

               
      crop: function(data) { //裁剪操作回调
      }
  });
  var fileName; //选择上传的文件名
  $('#btn1').change(function(){
      var file = this.files[0];
      fileName = file.name;
      var reader = new FileReader();
      //reader回调，重新初始裁剪区
      reader.onload = function(){
          // 通过 reader.result 来访问生成的 DataURL
          var url = reader.result;
          //选择图片后重新初始裁剪区
          $image.cropper('reset', true).cropper('replace', url);
      };
      reader.readAsDataURL(file);
  });

  /*
   * 上传图片
   */
  $('#image_save').click(function() {
      var type = $image.attr('src').split(';')[0].split(':')[1];

      var canVas = $image.cropper("getCroppedCanvas", {});
      //将裁剪的图片加载到face_image
      $('#avatar_preview').attr('src', canVas.toDataURL());
      canVas.toBlob(function(blob) {
          var formData = new FormData($("#save")[0]);
          //var username=$("#username").val();
          formData.append("image", blob, fileName);
          //alert(formData);
          //formData.append("username",username);

          $.ajax({
              type: "POST",
              url: '/accounts/changeavatar/',
              data: formData,
              contentType: false, //必须
              processData: false, //必须
              dataType: "json",
              success: function(data){
                  //清空上传文件的值
                 
                  $('#btn1').val('');


                  //上传成功
                  //console.log('retJson:', retJson);
                   alert('头像保存成功');
              },
              error : function() {
                  //清空上传文件的值
                  // $(_pageId + '#btn1').val('');
                  alert("11");
              }
          });
      }, type);
  });

  //取消
  $("#image_cancel").click(function() {
    //清空上传文件的值
    $(_pageId + inputFileId).val('');
  });
});/**
 * cropper图片上传
 */
$(function() {
  console.log('cropper图片上传。。。');

  //触发input file
  $('#upload_btn1').click(function() {
    console.log('模拟点击。。。');
    $('#btn2').trigger('click');
  });

  //图片上传
  var $image1 = $('.upload-img1 > img');
  $image1.cropper({
      viewMode: 1,
//      preview: '.img-preview', //不同尺寸预览区
      aspectRatio: 1, //裁剪比例，NaN-自由选择区域
      autoCropArea: 0.7, //初始裁剪区域占图片比例
      dragMode: 'move',
      aspectRatio: 1 / 1,
      preview: '#avatar_preview1',
      movable: false,
      zoomable: false,
      minCropBoxWidth: 100,
      minCropBoxHeight: 100,  
      minContainerWidth: 100,
      minContainerHeight: 100, 
      minCanvasWidth: 100,
      minCanvasHeight: 100,  
               
      crop: function(data) { //裁剪操作回调
      }
  });
  var fileName1; //选择上传的文件名
  $('#btn2').change(function(){
      var file1 = this.files[0];
      fileName1 = file1.name;
      var reader = new FileReader();
      //reader回调，重新初始裁剪区
      reader.onload = function(){
          // 通过 reader.result 来访问生成的 DataURL
          var url = reader.result;
          //选择图片后重新初始裁剪区
          $image1.cropper('reset', true).cropper('replace', url);
      };
      reader.readAsDataURL(file1);
  });

  /*
   * 上传图片
   */
  $('#image_save1').click(function() {
      var type = $image1.attr('src').split(';')[0].split(':')[1];

      var canVas = $image1.cropper("getCroppedCanvas", {});
      //将裁剪的图片加载到face_image
      $('#avatar_preview1').attr('src', canVas.toDataURL());
      canVas.toBlob(function(blob) {
          var formData = new FormData($("#save1")[0]);
         
          formData.append("image", blob, fileName);

          $.ajax({
              type: "POST",
              url: '/accounts/changeavatar/',
              data: formData,
              contentType: false, //必须
              processData: false, //必须
              dataType: "json",
              success: function(retJson){
                  //清空上传文件的值
                  $('#btn2').val('');

                  //上传成功
                  console.log('retJson:', retJson);
              },
              error : function() {
                  //清空上传文件的值
                  $(_pageId + '#btn2').val('');
              }
          });
      }, type);
  });

  //取消
  $("#image_cancel1").click(function() {
    //清空上传文件的值
    $(_pageId + inputFileId).val('');
  });
});/**
 * cropper图片上传
 */
$(function() {
  console.log('cropper图片上传。。。');

  //触发input file
  $('#upload_btn2').click(function() {
    console.log('模拟点击。。。');
    $('#btn3').trigger('click');
  });

  //图片上传
  var $image2 = $('.upload-img2 > img');
  $image2.cropper({
      viewMode: 1,
//      preview: '.img-preview', //不同尺寸预览区
      aspectRatio: 1, //裁剪比例，NaN-自由选择区域
      autoCropArea: 0.7, //初始裁剪区域占图片比例
      dragMode: 'move',
      aspectRatio: 1 / 1,
      preview: '#avatar_preview2',
      movable: false,
      zoomable: false,
      minCropBoxWidth: 100,
      minCropBoxHeight: 100,  
      minContainerWidth: 100,
      minContainerHeight: 100, 
      minCanvasWidth: 100,
      minCanvasHeight: 100,  
               
      crop: function(data) { //裁剪操作回调
      }
  });
  var fileName1; //选择上传的文件名
  $('#btn3').change(function(){
      var file2 = this.files[0];
      fileName2 = file2.name;
      var reader = new FileReader();
      //reader回调，重新初始裁剪区
      reader.onload = function(){
          // 通过 reader.result 来访问生成的 DataURL
          var url = reader.result;
          //选择图片后重新初始裁剪区
          $image2.cropper('reset', true).cropper('replace', url);
      };
      reader.readAsDataURL(file2);
  });

  /*
   * 上传图片
   */
  $('#image_save2').click(function() {
      var type = $image2.attr('src').split(';')[0].split(':')[1];

      var canVas = $image2.cropper("getCroppedCanvas", {});
      //将裁剪的图片加载到face_image
      $('#avatar_preview2').attr('src', canVas.toDataURL());
      canVas.toBlob(function(blob) {
          var formData = new FormData($("#save2")[0]);
          formData.append("image", blob, fileName);

          $.ajax({
              type: "POST",
              url: '/accounts/changeavatar/',
              data: formData,
              contentType: false, //必须
              processData: false, //必须
              dataType: "json",
              success: function(retJson){
                  //清空上传文件的值
                  $('#btn3').val('');
                  alert('头像保存成功');

                  //上传成功
                  console.log('retJson:', retJson);
              },
              error : function() {
                  //清空上传文件的值
                  $(_pageId + '#btn3').val('');
              }
          });
      }, type);
  });

  //取消
  $("#image_cancel2").click(function() {
    //清空上传文件的值
    $(_pageId + inputFileId).val('');
  });
});
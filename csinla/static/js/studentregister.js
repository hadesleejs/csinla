function ref(){
     var url = "/captcha/refresh/";
     var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: "post",
        url: url,
//      data: "para="+para,  此处data可以为 a=1&b=2类型的字符串 或 json数据。
        data: {"csrfmiddlewaretoken":csrfmiddlewaretoken},
        cache: false,
        async : false,
        dataType: "json",
        success: function (data)
        {
          // alert(data.image_url);
            
             $(".captcha").attr("src",data.image_url);
 
          
        },
        error:function (data) {      
            alert("请求失败！");
        }
     });}
//弹出隐藏层
function ShowDiv(show_div,bg_div){
document.getElementById(show_div).style.display='block';
document.getElementById(bg_div).style.display='block' ;
var bgdiv = document.getElementById(bg_div);
bgdiv.style.width = document.body.scrollWidth;
// bgdiv.style.height = $(document).height();
$("#"+bg_div).height($(document).height());
};
//关闭弹出层
function CloseDiv(show_div,bg_div)
{
document.getElementById(show_div).style.display='none';
document.getElementById(bg_div).style.display='none';
};
function regis(){
    if($('#school option:selected').val()=="select"){
        alert("学校是必填项");
        return false;
    }
    else if(!$('#phone').val().match(/^(:?(:?\d+))$/)){
        alert("联系电话请填写数字");
        return false;
    }
    else if (document.getElementById("read").checked==false) {
        alert("请阅读相关条约并勾选");
        return false;
    }
    else{return true;}

    
    
}
 var a= $("#school").find('option:selected').text();
        $('#schooltxt').val(a);
function selectother(){
     var school=$('#school option:selected');
    if (school.val()=="OTHER") {
      $('#schooltxt').show();
      $('#school').hide();
      $('#schooltxt').val(null);
    }
    else{ var a= $("#school").find('option:selected').text();
        $('#schooltxt').val(a);}
}

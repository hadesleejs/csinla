
window.onload=function(){ 
    //$(".btn-group1").css("cursor","not-allowed");  
 de=getCookie("department");//(getCookie("名字"))
 su=getCookie("subject");
 start=getCookie("year_start");
 end=getCookie("year_end");
 $('#department').val(de);
 $('#subject').val(su);
 $('#year_start').val(start);
 $('#year_end').val(end);
 if (de==""||de==null||start==""||start==null) {
  $('#department').val("select");
  $('#subject').val("select");
  $('#year_start').val("select");
  $('#year_end').val("select");}
 else{$('#department').val(de);

 $('#year_start').val(start);
 $('#year_end').val(end);}
} 

function setCookie(c_name, value, expiredays) {
        var exdate = new Date();
        exdate.setTime(exdate.getTime() + expiredays * 3600 * 1000);
        document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString()) + ";path=/";
    }
    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            var c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) {
                    c_end = document.cookie.length;
                }
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
    }
   
function selehide1(){
  $("#subject_list li").show();
}
  function selehide(){
   $("#subject_list li").hide();
  var obj_lis = $("#department_list li");
    for(i=0;i<obj_lis.length;i++){
        obj_lis[i].onclick = function(){
         $("#department").val(this.innerText);
        

        
  document.getElementById("subject").disabled=false;
  $(".btn-group1").css("cursor","default"); 
  $("#subject").val("select");
  
   var department = this.innerText;
   department=department.replace(/\s/g,'');


   $('.'+department).css('display','block');}
 
    }
       

    }
    function hidedepartment(){
     $("#hidedepartment").hide();
     $("#showdepartment").show();
     $("#department").hide();
     // $("#subjectid").css("width","100%");
     // $("#subjectid span").css("margin-left","0px")
     // $("#subjectid input").css("width","89%");
     // $("#subjectid input").css("margin-left", "10px");
     // $("#subject_list li").show();
     // $("#subject_list").css("width","89%");
     // $("#subject_list").css("margin-left","70px");

 }
 function showdepartment(){
     $("#hidedepartment").show();
     $("#showdepartment").hide();
     $("#department").show();
     // $("#departmentid").hide();
     // $("#subjectid").css("width","100%");
     // $("#subjectid span").css("margin-left","0px")
     // $("#subjectid input").css("width","89%");
     // $("#subjectid input").css("margin-left", "10px");
     // $("#subject_list li").show();
     // $("#subject_list").css("width","89%");
     // $("#subject_list").css("margin-left","70px");

 }
   
 function subject(){
        var obj_lis1 = $("#subject_list li");
    for(i=0;i<obj_lis1.length;i++){
        obj_lis1[i].onclick = function(){
          $("#subject").val(this.innerText);
         
        }}}

function y_start(){
   var start = $("#year_start_list li");
    for(i=0;i<start.length;i++){
        start[i].onclick = function(){
          $("#year_start").val(this.innerText);
         
        }}}
function y_end(){
     var end = $("#year_end_list li");
    for(i=0;i<end.length;i++){
        end[i].onclick = function(){
          $("#year_end").val(this.innerText);
         
        }}}



 
   
   
    
    function tableshow(a){
      if($('.moreinformation'+a).css("display")=="none"){
       $('.moreinformation'+a).toggle();
       $(".tabledown"+a).show();
       $(".tableup"+a).hide();
        $(".moreinformation"+a).show();}
        else{
          $(".moreinformation"+a).hide();
          $(".tabledown"+a).hide();
           $(".tableup"+a).show();
      }
    }
    
 
  // $(function($) {

  //     document.getElementById("subject").disabled=true;
      
   
       
  //   });
  function total(){
    if($('#c_table tr').find('td:eq(5)').css("display")=="none"){
        $('#c_table tr').find('td:eq(5)').show();
        $('#c_table tr').find('td:eq(6)').show();
        $('#c_table tr').find('td:eq(6)').css('border-right','1px dashed #000');
        $('#c_table tr').find('td:eq(2)').css('border-left','1px dashed #000');
        $('.listab').css('border','0');
        $('.lista').css('border','0');
        $('.listab').css('border-bottom','1px dashed #000');
        $('.lista').css('border-bottom','1px dashed #000');
        $('#c_table tr:last').find('td:eq(2)').css('border-bottom','1px dashed #000');
        $('#c_table tr:last').find('td:eq(3)').css('border-bottom','1px dashed #000');
        $('#c_table tr:last').find('td:eq(4)').css('border-bottom','1px dashed #000');
        $('#c_table tr:last').find('td:eq(5)').css('border-bottom','1px dashed #000');
        $('#c_table tr:last').find('td:eq(6)').css('border-bottom','1px dashed #000');

    }
    else{ $('#c_table tr').find('td:eq(5)').hide();
        $('#c_table tr').find('td:eq(6)').hide();
        $('#c_table tr').find('td:eq(2)').css('border','0');
        $('.listab').css('border','0');
        $('.lista').css('border','0');
        $('#c_table tr:last').find('td:eq(2)').css('border-bottom','0');
        $('#c_table tr:last').find('td:eq(3)').css('border-bottom','0');
        $('#c_table tr:last').find('td:eq(4)').css('border-bottom','0');
        $('#c_table tr:last').find('td:eq(5)').css('border-bottom','0');
        $('#c_table tr:last').find('td:eq(6)').css('border-bottom','0');
      }
    }
   
  $('#myCarousel').carousel('cycle');
  $('.carousel').carousel({
  interval: 500
});
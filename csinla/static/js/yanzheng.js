 if($(":radio[name='district']:checked").val()=="OTHER"){
    $('#loc5txt').show();
  }
   if($(":radio[name='house_type']:checked").val()=="other"){
     $('#house5txt').show();
     }
    if($(":radio[name='room_type']:checked").val()=="other"){
      $('#rent4txt').show();
     }
   function PRent(){
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
     //  else if($('#myEditor').val()==""){
     //  alert("详细内容是必填项");
     // }
     return ture;
     
   }
    function mPRent(){
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
     else if($('#mfee').val()==""){
      alert("月租是必填项");
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
     // else if($('.mmyEditor').val()==""){
     //  alert("详细内容是必填项");
     // }
    return true;
   }
     $('#house5').click(function(){
         $('#house5txt').show();
    });
    $('#rent4').click(function(){
         $('#rent4txt').show();
    });
    $('#loc5').click(function(){
         $('#loc5txt').show();
    });
    var a= $('#mlocal option:selected');
     var b=$('#mhouse option:selected');
     var c=$('#mrent option:selected');
    if (a.val()=="OTHER") {
      $('#mlocaltxt').show();
      $('#mlocal').hide();
    }
    if (b.val()=="other") {
      $('#mhousetxt').show();
      $('#mhouse').hide();
    }
    if (c.val()=="other") {
      $('#mrenttxt').show();
      $('#mrent').hide();
    }
     function selectother(){
     var a= $('#mlocal option:selected');
     var b=$('#mhouse option:selected');
     var c=$('#mrent option:selected');
    if (a.val()=="OTHER") {
      $('#mlocaltxt').show();
      $('#mlocal').hide();
    }
    if (b.val()=="other") {
      $('#mhousetxt').show();
      $('#mhouse').hide();
    }
    if (c.val()=="other") {
      $('#mrenttxt').show();
      $('#mrent').hide();
    }
  }
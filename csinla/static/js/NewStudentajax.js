
   


$("#uscapplybtn").click(function(){
  var formdata=new FormData($("#uscform")[0]);
  $.ajax({
    cache:false,
    type:"POST",
    url:"/accounts/add_apply/",
    data:formdata,
    async:true,
    processData:false,
    contentType:false,
    success:function(data){
      alert(data.msg);
    }
  });
})
$("#uclaapplybtn").click(function(){
  var formdata1=new FormData($("#uclaform")[0]);
  $.ajax({
    cache:false,
    type:"POST",
    url:"/accounts/add_apply/",
    data:formdata1,
    async:true,
    processData:false,
    contentType:false,
    success:function(data){
      alert(data.msg);
    }
  });
})
$("#ucsbapplybtn").click(function(){
  var formdata2=new FormData($("#ucsbform")[0]);
  $.ajax({
    cache:false,
    type:"POST",
    url:"/accounts/add_apply/",
    data:formdata2,
    async:true,
    processData:false,
    contentType:false,
    success:function(data){
      alert(data.msg);
    }
  });
})
$("#uciapplybtn").click(function(){
  var formdata3=new FormData($("#uciform")[0]);
  $.ajax({
    cache:false,
    type:"POST",
    url:"/accounts/add_apply/",
    data:formdata3,
    async:true,
    processData:false,
    contentType:false,
    success:function(data){
      alert(data.msg);
    }
  });
})

$("#mapplybtn").click(function(){
  $.ajax({
    cache:false,
    type:"POST",
    url:"/accounts/add_apply/",
    data:$("#mbform").serialize(),
    async:true,
    success:function(data){
      alert(data.msg);
    }
  });
})




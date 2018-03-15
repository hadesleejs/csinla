  var emailReg = /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/;
   function contactus(){
    if($("#emailtxt").val()==""){
      sAlert("请输入你的Email");
      return false;
    }
    else if( !emailReg.test($("#emailtxt").val()) ){
      sAlert("您输入的Email地址格式不正确！");
      return false;
    }
    else if($("#content").val()==""){
      sAlert("请填写你的信息");
      return false;
    }
    else{
      return true;
    }
   }
  function sAlert(str){ 
    var msgw,msgh,bordercolor; 
    msgw=400;//Width
    msgh=130;//Height 
    titleheight=25 //title Height
    bordercolor="#336699";//boder color
    titlecolor="#99CCFF";//title color
   
    var sWidth,sHeight; 
    sWidth=document.body.offsetWidth; 
    sHeight=screen.height; 
    var bgObj=document.createElement("div"); 
    bgObj.setAttribute('id','bgDiv'); 
    bgObj.style.position="fixed"; 
    bgObj.style.top="0"; 
    bgObj.style.background="#000"; //#777
    bgObj.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75";//progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75 
    bgObj.style.opacity="0.6"; 
    bgObj.style.left="0"; 
    bgObj.style.width=sWidth + "px"; 
    bgObj.style.height=sHeight + "px"; 
    bgObj.style.zIndex = "10000"; 
    document.body.appendChild(bgObj); 
     
    var msgObj=document.createElement("div") 
    msgObj.setAttribute("id","msgDiv"); 
    msgObj.setAttribute("align","center"); 
    msgObj.style.background="white"; 
    msgObj.style.border="1px solid " + bordercolor; 
    msgObj.style.position = "fixed"; 
    msgObj.style.left = "50%"; 
    msgObj.style.top = "50%"; 
    msgObj.style.font="12px/1.6em Verdana, Geneva, Arial, Helvetica, sans-serif"; 
    msgObj.style.marginLeft = "-225px" ; 
    msgObj.style.marginTop = -75+document.documentElement.scrollTop+"px"; 
    msgObj.style.width = msgw + "px"; 
    msgObj.style.height =msgh + "px"; 
    msgObj.style.textAlign = "center"; 
    msgObj.style.lineHeight ="25px"; 
    msgObj.style.zIndex = "10001"; 
     
    var title=document.createElement("h4"); 
    title.setAttribute("id","msgTitle"); 
    title.setAttribute("align","right"); 
    title.style.margin="0"; 
    title.style.padding="3px"; 
    title.style.background=''; 
    title.style.filter="";//progid:DXImageTransform.Microsoft.Alpha(startX=20, startY=20, finishX=100, finishY=100,style=1,opacity=75,finishOpacity=100); 
    title.style.opacity=""; //0.75
    title.style.border=''; 
    title.style.height="18px"; 
    title.style.font="12px Verdana, Geneva, Arial, Helvetica, sans-serif"; 
    title.style.color="black"; 
    title.style.cursor="pointer"; 
    title.innerHTML="X"; 
    title.onclick=function(){ 
           document.body.removeChild(bgObj); 
           document.getElementById("msgDiv").removeChild(title); 
           document.body.removeChild(msgObj); 
         } 
    document.body.appendChild(msgObj); 
    document.getElementById("msgDiv").appendChild(title); 
    var txt=document.createElement("p"); 
    txt.style.margin="1em 0" 
    txt.style.font="16px 微软雅黑"
    txt.setAttribute("id","msgTxt"); 
    txt.innerHTML=str+'<br><button id="close" class="btn" style="margin-top:20px;">确定</button>'; 
    document.getElementById("msgDiv").appendChild(txt); 
    document.getElementById("close").onclick=function(){ 
           document.body.removeChild(bgObj); 
           document.getElementById("msgDiv").removeChild(title); 
           document.body.removeChild(msgObj); 
         } 

 } 

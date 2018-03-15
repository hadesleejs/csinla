username=getCookie("username");//(getCookie("名字"))
password=getCookie("password");
 
 $('#username').val(username);
 $('#password').val(password);
 musername=getCookie("musername");//(getCookie("名字"))
mpassword=getCookie("mpassword");
 
 $('#musername').val(musername);
 $('#mpassword').val(mpassword);

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
function save() {
  
if ($("input[type='checkbox']").is(':checked')==true) { 
  var username=$("#username").val();
  var password=$("#password").val();
  //alert(username);
  
 setCookie("username",username);//（名字=getCookie(名字)，需要存的值）
  setCookie("password", password);}}
  
  
  function msave() {
  
if ($("input[type='checkbox']").is(':checked')==true) { 
  
  var musername=$("#musername").val();
  var mpassword=$("#mpassword").val();
 
  setCookie("musername",musername);//（名字=getCookie(名字)，需要存的值）
  setCookie("mpassword", mpassword);}}
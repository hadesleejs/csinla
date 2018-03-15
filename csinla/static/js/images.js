function ImagePreviews(avalue) {

        var docObj = document.getElementById("qpicture-selector");

        var dd3 = document.getElementById("view1");

        dd3.innerHTML = "";

        var fileList = docObj.files;

        for (var i = 0; i < 10; i++) {            

          if(i<9){

            dd3.innerHTML += "<img id='img" + i + "'  />";

            var imgObjPreview = document.getElementById("img"+i); 
           }
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
function ImagePreviews1(avalue) {

        var docObj1 = document.getElementById("qpicture-selector2");

        var view2 = document.getElementById("view2");

        view2.innerHTML = "";

        var fileList1 = docObj1.files;

        for (var i = 0; i < 10; i++) {            

          if(i<9){

            view2.innerHTML += "<img id='img" + i + "'  />";

            var imgObjPreview = document.getElementById("img"+i); 
           }
            else{alert('只能上传9张');}
            

            if (docObj1.files && docObj1.files[i]) {

                //火狐下，直接设img属性

                imgObjPreview.style.display = 'block';

                imgObjPreview.style.width = '100%';

                imgObjPreview.style.height = '100%';

                //imgObjPreview.src = docObj.files[0].getAsDataURL();

                //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式

                imgObjPreview.src = window.URL.createObjectURL(docObj1.files[i]);

            }

            else {

                //IE下，使用滤镜

                docObj1.select();

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
    function ImagePreviews2(avalue) {

        var docObj2 = document.getElementById("qpicture-selector4");

        var view3 = document.getElementById("view3");

        view3.innerHTML = "";

        var fileList2 = docObj2.files;

        for (var i = 0; i < 10; i++) {            

          if(i<9){

            view3.innerHTML += "<img id='img" + i + "'  />";

            var imgObjPreview = document.getElementById("img"+i); 
           }
            else{alert('只能上传9张');}
            

            if (docObj2.files && docObj2.files[i]) {

                //火狐下，直接设img属性

                imgObjPreview.style.display = 'block';

                imgObjPreview.style.width = '100%';

                imgObjPreview.style.height = '100%';

                //imgObjPreview.src = docObj.files[0].getAsDataURL();

                //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式

                imgObjPreview.src = window.URL.createObjectURL(docObj2.files[i]);

            }

            else {

                //IE下，使用滤镜

                docObj2.select();

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
     function ImagePreviews3(avalue) {

        var docObj5 = document.getElementById("qpicture-selector5");

        var view5 = document.getElementById("view5");

        view5.innerHTML = "";

        var fileList5 = docObj5.files;

        for (var i = 0; i < 10; i++) {            

          if(i<9){

            view5.innerHTML += "<img id='img" + i + "'  />";

            var imgObjPreview = document.getElementById("img"+i); 
           }
            else{alert('只能上传9张');}
            

            if (docObj5.files && docObj5.files[i]) {

                //火狐下，直接设img属性

                imgObjPreview.style.display = 'block';

                imgObjPreview.style.width = '100%';

                imgObjPreview.style.height = '100%';

                //imgObjPreview.src = docObj.files[0].getAsDataURL();

                //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式

                imgObjPreview.src = window.URL.createObjectURL(docObj5.files[i]);

            }

            else {

                //IE下，使用滤镜

                docObj5.select();

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
      function ImagePreviews4(avalue) {

        var docObj6 = document.getElementById("qpicture-selector6");

        var view6 = document.getElementById("view6");

        view6.innerHTML = "";

        var fileList6 = docObj6.files;

        for (var i = 0; i < 10; i++) {            

          if(i<9){

            view6.innerHTML += "<img id='img" + i + "'  />";

            var imgObjPreview = document.getElementById("img"+i); 
           }
            else{alert('只能上传9张');}
            

            if (docObj6.files && docObj6.files[i]) {

                //火狐下，直接设img属性

                imgObjPreview.style.display = 'block';

                imgObjPreview.style.width = '100%';

                imgObjPreview.style.height = '100%';

                //imgObjPreview.src = docObj.files[0].getAsDataURL();

                //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式

                imgObjPreview.src = window.URL.createObjectURL(docObj6.files[i]);

            }

            else {

                //IE下，使用滤镜

                docObj6.select();

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
    function ImagePreviews5(avalue) {

        var docObj7 = document.getElementById("qpicture-selector7");

        var view7 = document.getElementById("view7");

        view7.innerHTML = "";

        var fileList7 = docObj7.files;

        for (var i = 0; i < 10; i++) {            

          if(i<9){

            view7.innerHTML += "<img id='img" + i + "'  />";

            var imgObjPreview = document.getElementById("img"+i); 
           }
            else{alert('只能上传9张');}
            

            if (docObj7.files && docObj7.files[i]) {

                //火狐下，直接设img属性

                imgObjPreview.style.display = 'block';

                imgObjPreview.style.width = '100%';

                imgObjPreview.style.height = '100%';

                //imgObjPreview.src = docObj.files[0].getAsDataURL();

                //火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式

                imgObjPreview.src = window.URL.createObjectURL(docObj7.files[i]);

            }

            else {

                //IE下，使用滤镜

                docObj7.select();

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
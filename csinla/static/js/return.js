       history.pushState(null,null,document.url);
       window.addEventListener('popstate',function(){
            history.pushState(null,null,'/');
            window.location.reload();

       })
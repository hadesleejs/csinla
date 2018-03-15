$('#qtime').flatpickr({
        enableTime: true
    });
    $('#lv4').click(function(){
       $('#lv4txt').show();
    });
    $('#type4').click(function(){
       $('#type4txt').show();
    });
    function selectother(){
     var a= $('#mtype option:selected');
     var b=$('#mlevel option:selected');
    if (a.val()=="其他") {
      $('#mtypetxt').show();
      $('#mtype').hide();
    }
    if (b.val()=="其他") {
      $('#mleveltxt').show();
      $('#mlevel').hide();
    }
    
  }
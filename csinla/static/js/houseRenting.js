
/*
 * 搜索栏的方块
 * */
$(".u-main-search .duration span").on("click", function () {
    $(".u-main-search .duration span").removeClass("u-block");
    $(this).addClass("u-block")
});

/*
 * 展开评论、收起评论
 */
var parseEmotion = false;
$(".toggleComment").on("click", function () {
    var comments = $(".u-main-content .u-main-section .list-group");
    var length = comments.children().length;

    for (var i = 1; i < length - 1; i++) {
        comments.children().eq(i).toggleClass("hide");
    }

    // 首次展开评论时，解析表情
    if (parseEmotion == false) {
        for (var j = 1; j < length - 2; j++) {
            var item = comments.children().eq(j).children(".u-comment-content").children(".u-comment-text");
            item.html(item.html()).parseEmotion();
        }
        parseEmotion = true;
    }

    if ($(this).data("flag") == true) {
        $(this).data("flag", false);
        $(this).html("展开评论<i class='fa fa-angle-double-down'></i>");
    } else {
        $(this).data("flag", true);
        $(this).html("收起评论<i class='fa fa-angle-double-up'></i>");
    }
});

/*
 * 展开、收起回复
 * */
 
  if ($(".replyButton").html() == "收起回复") {
        
        
        $(".replyButton").html("收起回复").css({
            "border": "2px solid #dfdfdf",
            "border-bottom": "10px solid white"
        });
        $(".replyButton").siblings(".u-reply").show();}
       
  else {
        $(".replyButton").html("回复").css({
            "border": 0
        });
        $(".replyButton").removeClass("borderButton");
        $(".replyButton").siblings(".u-reply").hide();
  }

$(".replyButton").on("click", function () {
    if ($(this).html() == "回复") {
        $(this).html("收起回复").css({
            "border": "2px solid #dfdfdf",
            "border-bottom": "10px solid white"
        });
        $(this).siblings(".u-reply").show();
    } else {
        $(this).html("回复").css({
            "border": 0
        });
        $(this).removeClass("borderButton");
        $(this).siblings(".u-reply").hide();
    }
});

/*
 * 点赞
 * */
$(".likeIt").on("click", function () {
    $(this).toggleClass('like');
});

// /*
//  * map
//  */
// // 百度地图API功能
// function G(id) {
//     return document.getElementById(id);
// }

// var map = new BMap.Map("baiduMap");
// map.centerAndZoom(new BMap.Point(116.404, 39.915), 15);

// // ------------------------------------------------------
// var ac = new BMap.Autocomplete(    //建立一个自动完成的对象
//     {
//         "input": "suggestId"
//         , "location": map
//     });

// ac.addEventListener("onhighlight", function (e) {  //鼠标放在下拉列表上的事件
//     var str = "";
//     var _value = e.fromitem.value;
//     var value = "";
//     if (e.fromitem.index > -1) {
//         value = _value.province + _value.city + _value.district + _value.street + _value.business;
//     }
//     str = "FromItem<br />index = " + e.fromitem.index + "<br />value = " + value;

//     value = "";
//     if (e.toitem.index > -1) {
//         _value = e.toitem.value;
//         value = _value.province + _value.city + _value.district + _value.street + _value.business;
//     }
//     str += "<br />ToItem<br />index = " + e.toitem.index + "<br />value = " + value;
//     G("searchResultPanel").innerHTML = str;
// });

// var myValue;
// ac.addEventListener("onconfirm", function (e) {    //鼠标点击下拉列表后的事件
//     var _value = e.item.value;
//     myValue = _value.province + _value.city + _value.district + _value.street + _value.business;
//     G("searchResultPanel").innerHTML = "onconfirm<br />index = " + e.item.index + "<br />myValue = " + myValue;

//     setPlace();
// });

// function setPlace() {
//     map.clearOverlays();    //清除地图上所有覆盖物
//     function myFun() {
//         var pp = local.getResults().getPoi(0).point;    //获取第一个智能搜索的结果
//         map.centerAndZoom(pp, 18);
//         map.addOverlay(new BMap.Marker(pp));    //添加标注
//     }

//     var local = new BMap.LocalSearch(map, { //智能搜索
//         onSearchComplete: myFun
//     });
//     local.search(myValue);
// }

// // 定位到所在城市------------------------------------------------------------
// function setLocaleCity(result) {
//     var cityName = result.name;
//     map.setCenter(cityName);   //关于setCenter()可参考API文档---”传送门“
// }
// var myCity = new BMap.LocalCity();
// myCity.get(setLocaleCity);

// map.enableScrollWheelZoom();   //启用滚轮放大缩小，默认禁用

// //添加控件和比例尺------------------------------------------------------------
// var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
// var top_left_navigation = new BMap.NavigationControl();  //左上角，添加默认缩放平移控件
// map.addControl(top_left_control);
// map.addControl(top_left_navigation);

// // 添加定位控件----------------------------------------------------------------
// var geolocationControl = new BMap.GeolocationControl();
// map.addControl(geolocationControl);

// // 全景图-------------------------------------------------------------------
// // 覆盖区域图层测试
// map.addTileLayer(new BMap.PanoramaCoverageLayer());

// var stCtrl = new BMap.PanoramaControl(); //构造全景控件
// stCtrl.setOffset(new BMap.Size(20, 20));
// map.addControl(stCtrl);//添加全景控件

// // 浏览器自动定位------------------------------------------------------------
// var localServiceSearchPoint = null;
// var geolocation = new BMap.Geolocation();
// geolocation.getCurrentPosition(function (r) {
//     if (this.getStatus() == BMAP_STATUS_SUCCESS) {
//         var mk = new BMap.Marker(r.point);
//         map.addOverlay(mk);
//         map.panTo(r.point);
//         localServiceSearchPoint = r.point;
// //            alert('您的位置：'+r.point.lng+','+r.point.lat);
//     }
//     else {
// //            alert('failed'+this.getStatus());
//     }
// }, {enableHighAccuracy: true});

// // 从这里开始是自定义的功能----------------------------------------------------
// var local = new BMap.LocalSearch(map,
//     {renderOptions: {map: map, autoViewport: true}});

// var localService = [];  // 本地服务类型
// var services = $("input[type='checkbox'][name='service']");
// services.on("click", function () {
//     localService = [];
//     for (var i = 0; i < services.length; i++) {
//         var item = services.eq(i);
//         if (item.is(":checked")) {
//             localService.push(item.val());
//         }
//     }
//     // 需要获取当前位置
//     local.searchNearby(localService, localServiceSearchPoint);
// });

// function initAutocomplete() {
//   var map = new google.maps.Map(document.getElementById('map'), {
//     center: {lat: -33.8688, lng: 151.2195},
//     zoom: 13,
//     mapTypeId: google.maps.MapTypeId.ROADMAP
//   });

//   // Create the search box and link it to the UI element.
//   var input = document.getElementById('pac-input');
//   var searchBox = new google.maps.places.SearchBox(input);
//   map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

//   // Bias the SearchBox results towards current map's viewport.
//   map.addListener('bounds_changed', function() {
//     searchBox.setBounds(map.getBounds());
//   });

//   var markers = [];
//   // [START region_getplaces]
//   // Listen for the event fired when the user selects a prediction and retrieve
//   // more details for that place.
//   searchBox.addListener('places_changed', function() {
//     var places = searchBox.getPlaces();

//     if (places.length == 0) {
//       return;
//     }

//     // Clear out the old markers.
//     markers.forEach(function(marker) {
//       marker.setMap(null);
//     });
//     markers = [];

//     // For each place, get the icon, name and location.
//     var bounds = new google.maps.LatLngBounds();
//     places.forEach(function(place) {
//       var icon = {
//         url: place.icon,
//         size: new google.maps.Size(71, 71),
//         origin: new google.maps.Point(0, 0),
//         anchor: new google.maps.Point(17, 34),
//         scaledSize: new google.maps.Size(25, 25)
//       };

//       // Create a marker for each place.
//       markers.push(new google.maps.Marker({
//         map: map,
//         icon: icon,
//         title: place.name,
//         position: place.geometry.location
//       }));

//       if (place.geometry.viewport) {
//         // Only geocodes have viewport.
//         bounds.union(place.geometry.viewport);
//       } else {
//         bounds.extend(place.geometry.location);
//       }
// var pyrmont = place.geometry.location;

// var service = new google.maps.places.PlacesService(map);
// var localService = [];  // 本地服务类型
// var services = $("input[type='checkbox'][name='service']");
// services.on("click", function () {
//     localService = [];
//     for (var i = 0; i < services.length; i++) {
//         var item = services.eq(i);
//         if (item.is(":checked")) {
//             // localService.push(item.val());
//          initialize(item, pyrmont);
//         }
//     }
//     // 需要获取当前位置
//     // local.searchNearby(localService, localServiceSearchPoint);
// });
  

//     });
//     map.fitBounds(bounds);
  


//   });
//   // [END region_getplaces]


// }

// function initialize(item,places) {

//   // var pyrmont = {lat: -33.867, lng: 151.195};
//   map = new google.maps.Map(document.getElementById('map'), {
//     center: places,
//     zoom: 15
//   });

//   infowindow = new google.maps.InfoWindow();

//   var service = new google.maps.places.PlacesService(map);
//   service.nearbySearch({
//     location: places,
//     radius: 500,
//     types: item
//   }, callback);

// }



// function callback(results, status) {
//   if (status === google.maps.places.PlacesServiceStatus.OK) {
//     for (var i = 0; i < results.length; i++) {
//       createMarker(results[i]);
//     }
//   }
// }

// function createMarker(place) {
//   var placeLoc = place.geometry.location;
//   var marker = new google.maps.Marker({
//     map: map,
//     position: place.geometry.location
//   });

//   google.maps.event.addListener(marker, 'click', function() {
//     infowindow.setContent(place.name);
//     infowindow.open(map, this);
//   });
// }

// /*
//  * sinaEmotion
//  * */
// $("#emotion").on("click", function (event) {
//     if (!$('#sinaEmotion').is(':visible')) {
//         $(this).sinaEmotion();
//         event.stopPropagation();
//     }
// });
// function initMap() {

//   var map = new google.maps.Map(document.getElementById('map'), {
//     zoom: 8
   
//   });
//   var geocoder = new google.maps.Geocoder;
//   geocoder.geocode({'address': 'USA'}, function(results, status) {
//     if (status === google.maps.GeocoderStatus.OK) {
//       map.setCenter(results[0].geometry.location);
//       new google.maps.Marker({
//         map: map,
//         position: results[0].geometry.location
//       });
//     } else {
//       window.alert('Geocode was not successful for the following reason: ' +
//           status);
//     }
//   });
// }



       /**
        * @constructor
       */
      function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: -34.397, lng: 150.644},
          zoom: 6
        });
        var infoWindow = new google.maps.InfoWindow({map: map});
        var geocoder = new google.maps.Geocoder;
        geocoder.geocode({'address': addres}, function(results, status) {
          if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            new google.maps.Marker({
              map: map,
              position: results[0].geometry.location
            });
          } else {
            window.alert('Geocode was not successful for the following reason: ' +
                status);
          }
           new AutocompleteDirectionsHandler(map);
        });
      

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('你所在的位置.');
            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }

      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
      }

      function AutocompleteDirectionsHandler(map) {
        this.map = map;
        this.originPlaceId = null;
        this.destinationPlaceId = null;
        this.travelMode = 'WALKING';
        var originInput = document.getElementById('origin-input');
        var destinationInput = document.getElementById('destination-input');
        var modeSelector = document.getElementById('mode-selector');
        this.directionsService = new google.maps.DirectionsService;
        this.directionsDisplay = new google.maps.DirectionsRenderer;
        this.directionsDisplay.setMap(map);

        var originAutocomplete = new google.maps.places.Autocomplete(
            originInput, {placeIdOnly: true});
        var destinationAutocomplete = new google.maps.places.Autocomplete(
            destinationInput, {placeIdOnly: true});

        this.setupClickListener('changemode-walking', 'WALKING');
        this.setupClickListener('changemode-transit', 'TRANSIT');
        this.setupClickListener('changemode-driving', 'DRIVING');

        this.setupPlaceChangedListener(originAutocomplete, 'ORIG');
        this.setupPlaceChangedListener(destinationAutocomplete, 'DEST');

        this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(originInput);
        this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(destinationInput);
        this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(modeSelector);
      }

      // Sets a listener on a radio button to change the filter type on Places
      // Autocomplete.
      AutocompleteDirectionsHandler.prototype.setupClickListener = function(id, mode) {
        var radioButton = document.getElementById(id);
        var me = this;
        radioButton.addEventListener('click', function() {
          me.travelMode = mode;
          me.route();
        });
      };

      AutocompleteDirectionsHandler.prototype.setupPlaceChangedListener = function(autocomplete, mode) {
        var me = this;
        autocomplete.bindTo('bounds', this.map);
        autocomplete.addListener('place_changed', function() {
          var place = autocomplete.getPlace();
          if (!place.place_id) {
            window.alert("Please select an option from the dropdown list.");
            return;
          }
          if (mode === 'ORIG') {
            me.originPlaceId = place.place_id;
          } else {
            me.destinationPlaceId = place.place_id;
          }
          me.route();
        });

      };

      AutocompleteDirectionsHandler.prototype.route = function() {
        if (!this.originPlaceId || !this.destinationPlaceId) {
          return;
        }
        var me = this;

        this.directionsService.route({
          origin: {'placeId': this.originPlaceId},
          destination: {'placeId': this.destinationPlaceId},
          travelMode: this.travelMode
        }, function(response, status) {
          if (status === 'OK') {
            me.directionsDisplay.setDirections(response);
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
      };
      window.onscroll = function () { 
 $("#ac").css('top','0px');
};
$(function(){
    //picturesEyes($('li'));
    $('.bigimg').picEyes();
    $('.bigimage').picEyes();
});
var myplace,infowindow,marker;
    var myLatlng=new google.maps.LatLng(30, 120);
    var mapOptions = {
      center: myLatlng,
      zoom: 13,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map"),
        mapOptions);
        
    $(document).ready(function(){
        //jQuery捕获点击动作
            myplace=$("#addres").text();//获取输入的地址
            //alert(myplace);
            var geocoder = new google.maps.Geocoder();//创建geocoder服务
            /* 调用geocoder服务完成转换 */
            geocoder.geocode( { 'address': myplace}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });
                infowindow = new google.maps.InfoWindow({
                    content: myplace,
                    maxWidth: 200
                });
                google.maps.event.addListener(marker, 'click', function() {
                    infowindow.open(map,marker);
                });
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
            });
        });
   
    
  if($("#map").html()==''){
    $("#map").hide();
  }
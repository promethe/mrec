var initialLocation;
var map;

function initialize() {
    var myOptions = {
      zoom: 16,
      center: initialLocation,
      disableDefaultUI: true,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error);
    } else {
        error('not supported');
    }
}

function success(position) {
    // add success notification
    initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
    map.setCenter(initialLocation);

    $('input[name=longitude]').val(position.coords.longitude);
    $('input[name=latitude]').val(position.coords.latitude);
}

function error(msg) {
  alert('Couldn\'t localize the device using Webkit!');
  // console.log(arguments);
}    

function detectBrowser() {
  var useragent = navigator.userAgent;
  var mapdiv = document.getElementById("map_canvas");
    
  if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1 ) {
    mapdiv.style.width = '100%';
    mapdiv.style.height = '100%';
  } else {
    mapdiv.style.width = '600px';
    mapdiv.style.height = '800px';
  }
}

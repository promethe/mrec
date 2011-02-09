if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(success, error);
} else {
  error('not supported');
}

function success(position) {
    alert("Zecholokowany!");
    // $('#status').removeClass('fail');
    $('input[name=longitude]').val(position.coords.longitude);
    $('input[name=latitude]').val(position.coords.latitude);
    
    // 
    // if (jQuery) {  
    //    alert("Hello!");
    // } else {
    //     alert("Not loaded!");
    // }
    // 
    // $('divstatus').addClass('success');
    // 
    // document.querySelector('#longitude').value = position.coords.longitude
    // document.querySelector('#latitude').value = position.coords.latitude

}

function error(msg) {
  alert('fail!');
  // console.log(arguments);
}
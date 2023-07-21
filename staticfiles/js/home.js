// toogler

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}





var marker;

function initMap(lat, lng) {
    var myLatLng = {lat: lat, lng: lng};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: myLatLng
    });
    marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'My Location'
    });
}

console.log("hello")




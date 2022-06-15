
function initialize() {
  const location = { lat: latval, lng: lngval };
//   const map = new google.maps.Map(document.getElementById("map"), {
//     center: location,
//   });

//   console.log(location)
  const panorama = new google.maps.StreetViewPanorama(
    document.getElementById("pano"),
    {
      position: location,
      addressControl: false,
      panControl: false,
      showRoadLabels: false,
    }
  );
}

// console.log(latval)
// console.log(lngval)

window.initialize = initialize;
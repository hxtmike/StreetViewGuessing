
function initialize() {
//   const map = new google.maps.Map(document.getElementById("map"), {
//     center: location,
//   });

//   console.log(location)
  const panorama = new google.maps.StreetViewPanorama(
    document.getElementById("pano"),
    {
      pano: rst['panoId'],
      addressControl: false,
      panControl: false,
      showRoadLabels: false,
    }
  );
}

// console.log(latval)
// console.log(lngval)

window.initialize = initialize;
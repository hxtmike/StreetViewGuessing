for (let i = 0; i < favourites.length; i++) {

    var element = document.createElement('tr');

    element.innerHTML = "<td>" + favourites[i].lat + "</td><td>" + favourites[i].lon + "</td><td>" + favourites[i].state + "</td><td>" + favourites[i].pano + "</td><td>" + "<a href='https://www.google.com/maps/@?api=1&map_action=pano&pano=" + favourites[i].pano +"'>link</a>" + "</td>";

    document.getElementById("maintable").appendChild(element);
}
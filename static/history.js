for (let i = 0; i < history.length; i++) {

    var element = document.createElement('tr');

    element.innerHTML = "<td>" + history[i].timestamp + "</td><td>" + history[i].lat + "</td><td>" + history[i].lon + "</td><td>" + history[i].state + "</td><td>" + history[i].pano + "</td><td>" + "<a href='https://www.google.com/maps/@?api=1&map_action=pano&pano=" + history[i].pano +"'>link</a>" + "</td><td>" + "<a href='/favourites?lat=" + history[i].lat + '&lon=' + history[i].lon + '&state=' + history[i].state + '&pano=' + history[i].pano + "'>link</a>";

    document.getElementById("maintable").appendChild(element);
}
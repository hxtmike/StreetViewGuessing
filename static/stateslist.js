for (let i = 0; i < stateslist.length; i++) {

    var element = document.createElement('tr');

    element.innerHTML = "<td>" + stateslist[i].iso + "</td><td>" + stateslist[i].state + "</td><td>" + "<a href='/?state=" + stateslist[i].iso +"'>link</a>" + "</td>";

    document.getElementById("maintable").appendChild(element);
}
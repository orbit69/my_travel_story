var show_link_request = document.getElementById("myBtn");
show_link_request.onclick = function(){
    var req_box = document.getElementById("myModal");
    req_box.style.visibility="visible";
};

var close_request = document.getElementsByClassName("close")[0];
close_request.onclick = function () {
    var req_box = document.getElementById("myModal");
    req_box.style.visibility="hidden";
};

var sendLinkData = document.getElementById("link_generate");
sendLinkData.onclick = function(){
    var fromDate = document.getElementById("link_from");
    var toDate = document.getElementById("link_to");
    alert(fromDate.value + " " + toDate.value);
    
    var csrftoken = getCookie('csrftoken');
    var req = new XMLHttpRequest();
    req.open("POST","",true);
    req.setRequestHeader("X-CSRFToken",csrftoken);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("from="+fromDate.value+"&to="+toDate.value);
    req.onreadystatechange = function(){
        if(req.readyState==4 && req.status==200){
            var resString = "http://127.0.0.1:8000/mytravelstory/shared_link?data="+req.responseText;
            document.getElementById("result_link").innerHTML = resString;
        }
    };
};

function getMarkerData(){
    giveChildFunc();
    var csrftoken = getCookie('csrftoken');
    var req = new XMLHttpRequest();
    req.open("POST","",true);
    req.setRequestHeader("X-CSRFToken",csrftoken);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("action=1");
    req.onreadystatechange = function(){
        if(req.readyState==4 && req.status==200) {
            (function (window, google) {

                var json_data = JSON.parse(req.responseText);
                var staticMarkers = [];
                var staticInfos = [];

                //map options
                var options = {
                        center: {
                            lat: 50.066793,
                            lng: 19.913251
                        },
                        zoom: 17
                    },
                    element = document.getElementById('map-canvas');
                //map
                map = new google.maps.Map(element, options);

                for(var index=0; index<json_data.length;index++){
                   var markerPosition = {lat: json_data[index].fields.latitude, lng: json_data[index].fields.longtitude};

                    staticMarkers.push(new google.maps.Marker({
                        map: map,
                        position: markerPosition,
                        name: json_data[index].fields.name,
                        arrival: json_data[index].fields.arrival,
                        departure: json_data[index].fields.departure
                    }));

                    google.maps.event.addListener(staticMarkers[index], 'click', function() {
                        for(var i=0;i<staticInfos.length;i++){
                            staticInfos[i].close();
                        }
                        var si = new google.maps.InfoWindow();
                        staticInfos.push(si);
                    si.setContent(this.name + "</br>" +
                                    this.arrival + " - " + this.departure + "</br>" +
                                    '<input id="show_place" class="button" type="button" value="Show place" />');
                        si.open(map,this);
                        var button = document.getElementById("show_place");
                        button.addEventListener("click",showFromMap);
                    });
                }

                var input = /** @type {!HTMLInputElement} */(document.getElementById('search-text'));

                var autocomplete = new google.maps.places.Autocomplete(input);
                autocomplete.bindTo('bounds', map);

                var infowindow = new google.maps.InfoWindow();
                var marker = new google.maps.Marker({
                    map: map,
                    anchorPoint: new google.maps.Point(0, -29)
                });



                map.addListener('click', function (e) {
                    marker.setVisible(false);
                    infowindow.close();
                    var position = e.latLng;
                    marker.setPosition(position);
                    var address;
                    var geocoder = new google.maps.Geocoder();


                    geocoder.geocode({'latLng': position}, function (results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                            if (results[0]) {
                                address = results[0].formatted_address;
                                infowindow.setContent(results[0].formatted_address +
                                    '<br/><a href="add_place"><input id="add_place" class="button" type="button" value="Add place" /></a>');
                                marker.setIcon(/** @type {google.maps.Icon} **/ ({
                                    url: 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png',
                                    size: new google.maps.Size(71, 71),
                                    origin: new google.maps.Point(0, 0),
                                    anchor: new google.maps.Point(17, 34),
                                    scaledSize: new google.maps.Size(35, 35)

                                }));
                                marker.setVisible(true);
                                infowindow.open(map, marker);
                                document.getElementById("add_place").onclick = send_coordinates(position, address);
                            }
                            else {
                                return "No result";
                            }
                        }
                        else {
                            return status;
                        }
                    });
                });


                autocomplete.addListener('place_changed', function () {
                    infowindow.close();
                    marker.setVisible(false);
                    var place = autocomplete.getPlace();
                    if (!place.geometry) {
                        //user entered name of Place that was not suggested
                        window.alert("No details available for input: '" + place.name + "'");
                        return;
                    }

                    //if place has geometry
                    if (place.geometry.viewport) {
                        map.fitBounds(place.geometry.viewport);
                    } else {
                        map.setCenter(place.geometry.location);
                        map.setZoom(17);
                    }

                    marker.setIcon(/** @type {google.maps.Icon} **/ ({
                        url: 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png',
                        size: new google.maps.Size(71, 71),
                        origin: new google.maps.Point(0, 0),
                        anchor: new google.maps.Point(17, 34),
                        scaledSize: new google.maps.Size(35, 35)
                    }));

                    marker.setPosition(place.geometry.location);
                    marker.setVisible(true);

                    var address = '';
                    if (place.address_components) {
                        address = [
                            (place.address_components[0] && place.address_components[0].short_name || ''),
                            (place.address_components[1] && place.address_components[1].short_name || ''),
                            (place.address_components[2] && place.address_components[2].short_name || '')
                        ].join(' ');
                    }

                    infowindow.setContent('<div><strong>' + place.name + '</strong><br>' +
                        '<br/><a href="add_place"><input id="add_place" class="button" type="button" value="Add place"/> </a>');
                    infowindow.open(map, marker);

                    document.getElementById("add_place").onclick = send_coordinates(place.geometry.location, address);
                });
            }(window, google));

        }
    };


}



function showFromMap(){
    var date = this.previousSibling.previousSibling.nodeValue;
    var name = this.previousSibling.previousSibling.previousSibling.previousSibling.nodeValue;
    var csrftoken = getCookie('csrftoken');
    var req = new XMLHttpRequest();
    req.open("POST","",true);
    req.setRequestHeader("X-CSRFToken",csrftoken);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("mapName="+name+"&mapDate="+date);
    req.onreadystatechange = function(){
      if(req.readyState==4) {
          window.location.href = "show_place"
      }
    };
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function send_coordinates(position,address){
    var csrftoken = getCookie('csrftoken');
    var req = new XMLHttpRequest();
    req.open("POST","",true);
    req.setRequestHeader("X-CSRFToken",csrftoken);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("latLng="+String(position)+"&placeName="+address);
}

function sendPlaceData(){
    childElems = this.getElementsByTagName("p");
    var name = childElems[0].firstChild.nodeValue;
    var date = childElems[1].firstChild.nodeValue;
    var csrftoken = getCookie('csrftoken');
    var req = new XMLHttpRequest();
    req.open("POST","",true);
    req.setRequestHeader("X-CSRFToken",csrftoken);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("name="+name+"&date="+date);
    req.onreadystatechange = function(){
      if(req.readyState==4) {
          window.location.href = "show_place"
      }
    };
}

function giveChildFunc(){

    sideBar = document.getElementById("side-bar");

    sideBarChildren = sideBar.getElementsByTagName("div");

    for(var ind=0;ind<sideBar.childElementCount;ind++){
        sideBarChildren[ind].addEventListener("click", sendPlaceData);
    }
}


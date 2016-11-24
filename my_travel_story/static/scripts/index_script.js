(function(window,google){


    //map options
    var options = {
        center: {
            lat: 37.791350,
            lng: -122.435883
        },
        zoom: 10
    },
        element = document.getElementById('map-canvas');
    //map
    map = new google.maps.Map(element, options);

    google.maps.event.addDomListener(window, 'resize', function(){
        var center = map.getCenter();
        map.setCenter(center);
    });

    google.maps.event.trigger(map,"resize");
}(window,google));
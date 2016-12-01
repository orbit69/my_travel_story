(function(window,google){


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

    var input = /** @type {!HTMLInputElement} */(document.getElementById('search-text'));

    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds',map);

    var infowindow = new google.maps.InfoWindow();
    var marker = new google.maps.Marker({
        map: map,
        anchorPoint: new google.maps.Point(0,-29)
    });

    map.addListener('click',function(e){
        marker.setVisible(false);
        infowindow.close();
        var position = e.latLng;
        var address;
        marker.setPosition(position);

        var geocoder = new google.maps.Geocoder();


            geocoder.geocode( {'latLng': position}, function(results,status){
                if(status == google.maps.GeocoderStatus.OK) {
                    if (results[0]) {

                         infowindow.setContent(/*'<div><strong>' + place.name + '</strong><br>' +*/ results[0].formatted_address +
           '<br/><input id="add_place" class="button" type="button" value="Add place"/> ');
                         marker.setIcon(/** @type {google.maps.Icon} **/ ({
            url: 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png',
            size: new google.maps.Size(71,71),
            origin: new google.maps.Point(0,0),
            anchor: new google.maps.Point(17,34),
            scaledSize: new google.maps.Size(35,35)

        }));
                          marker.setVisible(true);
                        infowindow.open(map,marker);
                    }
                    else {
                        return  "No result";
                    }
                }
                else {
                    return status;
                }
            });








        //
    });

   

    autocomplete.addListener('place_changed', function(){
        infowindow.close();
        marker.setVisible(false);
        var place = autocomplete.getPlace();
        if(!place.geometry){
            //user entered name of Place that was not suggested
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }

        //if place has geometry
        if(place.geometry.viewport){
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }

        marker.setIcon(/** @type {google.maps.Icon} **/ ({
            url: 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png',
            size: new google.maps.Size(71,71),
            origin: new google.maps.Point(0,0),
            anchor: new google.maps.Point(17,34),
            scaledSize: new google.maps.Size(35,35)
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
            '<br/><input id="add_place" class="button" type="button" value="Add place"/> ');
          infowindow.open(map, marker);
    });
}(window,google));
          
                      (function (window, google) {

                          var json_data = JSON.parse(document.getElementById("places_data").innerHTML);
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

                          for (var index = 0; index < json_data.length; index++) {
                              var markerPosition = {
                                  lat: json_data[index].fields.latitude,
                                  lng: json_data[index].fields.longtitude
                              };

                              staticMarkers.push(new google.maps.Marker({
                                  map: map,
                                  position: markerPosition,
                                  name: json_data[index].fields.name,
                                  arrival: json_data[index].fields.arrival,
                                  departure: json_data[index].fields.departure
                              }));

                              google.maps.event.addListener(staticMarkers[index], 'click', function () {
                                  for (var i = 0; i < staticInfos.length; i++) {
                                      staticInfos[i].close();
                                  }
                                  var si = new google.maps.InfoWindow();
                                  staticInfos.push(si);
                                  si.setContent(this.name + "</br>" +
                                      this.arrival + " - " + this.departure + "</br>"
                                      );
                                  si.open(map, this);
                              });
                          }

                          var infowindow = new google.maps.InfoWindow();
                          var marker = new google.maps.Marker({
                              map: map,
                              anchorPoint: new google.maps.Point(0, -29)
                          });
                          

                      }(window, google));


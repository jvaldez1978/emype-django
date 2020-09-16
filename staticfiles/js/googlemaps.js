var map, infoWindow;
var myLayers; 
var bounds;
var overlay;
var gmarkers=[];
var glabels=[];
var zoom;
var oms;
var first_time = true;
var toggleMove = false;

function createMap(ruta, criterio){
    if (typeof ruta === 'undefined'){
        ruta = 0;
    } 
    if (typeof criterio === 'undefined'){
        criterio = 'empty';
    } 
    //overlay = new ItpOverlay("appbody");
    //overlay.show();
    var options = {
        center: {lat: -12.046374, lng: -77.042793},
        zoom: 12,
        //disableDefaultUI: true,
        streetViewControlOptions: {
              position: google.maps.ControlPosition.TOP_CENTER
          },
        mapTypeId: google.maps.MapTypeId.HYBRID,
        streetViewControl: true,            
        fullscreenControl: true,            
        fullscreenControlOptions: {
              position: google.maps.ControlPosition.TOP_RIGHT
          },
        mapTypeControl: true,
        mapTypeControlOptions: {
              style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
              position: google.maps.ControlPosition.TOP_CENTER
          },
        zoomControl: false,
        featureType: "poi",
    };

    bounds = new google.maps.LatLngBounds();
    myLayers = new google.maps.MVCObject();
    map = new google.maps.Map(document.getElementById('map'), options);
    //myLayers.set("POSTE NUEVO", map)

    /*var drawingManager = new google.maps.drawing.DrawingManager({
      drawingMode: google.maps.drawing.OverlayType.RECTANGLE,
      drawingControl: true,
      drawingControlOptions: {
        position: google.maps.ControlPosition.BOTTOM_CENTER,
        drawingModes: ['rectangle']
      },
      markerOptions: {icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'},
      circleOptions: {
        fillColor: '#ffff00',
        fillOpacity: 0.7,
        strokeWeight: 5,
        clickable: false,
        editable: true,
        zIndex: 1
      }
    });
    drawingManager.setMap(map);

    google.maps.event.addListener(drawingManager, 'overlaycomplete', function (OverlayCompleteEvent) {
        console.log(OverlayCompleteEvent.overlay);
        //bounds = null;
        bounds.extend(OverlayCompleteEvent.overlay.bounds.da);
        bounds.extend(OverlayCompleteEvent.overlay.bounds.ha);
        map.fitBounds(bounds);   
    });*/
    /*oms = new OverlappingMarkerSpiderfier(map, {
      markersWontMove: false,
      markersWontHide: false,
      basicFormatEvents: true
    });*/
    google.maps.event.addListener(map, 'click', function(event) {
        placeMarker(event.latLng);
     });
     
     function placeMarker(location) {
        clearMarkers();
        gmarkers = [];
         var marker = new google.maps.Marker({
             position: location, 
             map: map
         });
         gmarkers.push(marker);
         //console.log(gmarkers);
        }
    
        function setMapOnAll(map) {
            for (let i = 0; i < gmarkers.length; i++) {
                gmarkers[i].setMap(map);
            }
          }
          function clearMarkers() {
            setMapOnAll(null);
          }
    var body = document.body, html = document.documentElement;
    var height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
    document.getElementById('map').style.height = height + 'px';
}


function getInfo(identificador, latLng)
{
    overlay = new ItpOverlay("appbody");
    overlay.show();
    $.ajax({
        type: "GET",
        url: '/geoapp/get_infohtml/'+identificador,
        success: function(data) {
            overlay.hide();
            var infowindow = new google.maps.InfoWindow();
            //var myHTML = event.feature.getProperty("custom_icono");
            //var html = '<h2>'+id+'</h2>'
            infowindow.setContent(data);

            // position the infowindow on the marker
            infowindow.setPosition(latLng);
            // anchor the infowindow on the marker
            infowindow.setOptions({pixelOffset: new google.maps.Size(0,-30)});
            infowindow.open(map);    

        },
        error: function() {
            overlay.hide();
            console.log("No se ha podido obtener la información");
        }
    });
}


function recall_map(geojson){
    createMap;
}

function menu_totales(totales){
    for (var i = 0; i < totales.length; i++) {
        console.log(totales[i].idetapa + " " + totales[i].estructura);
        document.getElementById(totales[i].idetapa + " " + totales[i].estructura).innerHTML = "("+ totales[i].cant +")";
    }
}

function eqfeed_callback (geojson) {    
    for (var i = 0; i < geojson.features.length; i++) {
        addMarker(geojson.features[i], i);
    }

    map.addListener('bounds_changed',function() {
        ShowHideMarkers();
    });

    map.addListener('zoom_changed', function() {
        ShowHideMarkers();
    });
    //console.log(myLayers);
    if (first_time == false){
        if (i == 0){
            Swal.fire(
              'No se encontraron elementos para mostrar',
              'Intente con otra ruta',
              'info'
            )        
        }
    }
    else{
        first_time = false;
    }
    overlay.hide();
}

function ShowHideMarkers(){
    bounds = map.getBounds();
    zoom = map.getZoom();
    //console.log(zoom);
    //console.log(glabels);
    for (var i=0; i< gmarkers.length; i++) {
        //console.log(map.getZoom());
        //console.log(bounds.contains(gmarkers[i].getPosition()));
        //console.log();
        if (bounds.contains(gmarkers[i].getPosition())===false)
        {
            if (gmarkers[i].getVisible() === true)
                gmarkers[i].setVisible(false);    
        }
        else
        {
            if (gmarkers[i].getVisible() === false)
                gmarkers[i].setVisible(true);    
        }
        if (zoom < 16)
        {
            if (gmarkers[i].get("labelVisible") === true) 
                gmarkers[i].set("labelVisible", false)
            //gmarkers[i].setLabel(null);
        }         
        else{
            if (gmarkers[i].get("labelVisible") === false) 
                gmarkers[i].set("labelVisible", true)
            //gmarkers[i].setLabel('123');                
        }   
    }    
}

function ToggleDraggableMarker(){
    for (var i=0; i< gmarkers.length; i++) {
        if (gmarkers[i].get("draggable") == true){
            gmarkers[i].setDraggable(false);
            toggleMove = false;
            }
        else{
            gmarkers[i].setDraggable(true);
            toggleMove = true;
        }        
    }    
    if (toggleMove == true){
        $("#toggle-dragable").prop("title", "Desactivar mov. marcadores");
        $("#toggle-dragable").addClass('active');        
    }
    else {
        $("#toggle-dragable").prop("title", "Activar mov. marcadores");
        $("#toggle-dragable").removeClass('active');        
    }
}

function addMarker(data, i){
    var coords = data.geometry.coordinates;
    var latLng = new google.maps.LatLng(coords[1],coords[0]);
    var label = data.properties.item;
    var identificador = data.properties.identificador;

    var icon = {
        url: "/media/img/maps/"+data.properties.custom_icono,
        scaledSize: new google.maps.Size(data.properties.custom_icono_size, data.properties.custom_icono_size), // scaled size
        origin: new google.maps.Point(0,0), // origin
        anchor: new google.maps.Point(0, 0), // anchor
        labelOrigin: { x: 50, y: -50},        
    };    

    /*var marker = new google.maps.Marker({
        position: latLng,
        icon: icon,
        label: {
            text: label,
            color: 'white black',
            fontSize: "12px",
          }
    });*/     


    var marker = new MarkerWithLabel({
       position: latLng,
       draggable: toggleMove,
       raiseOnDrag: true,
       map: map,
       labelContent: label,
       labelAnchor: new google.maps.Point(5, -12),
       labelClass: "marker-label", // the CSS class for the label
       icon: icon,
     });

    /*google.maps.event.addListener(marker, 'spider_click', function(e) {  // 'spider_click', not plain 'click'
        getInfo(identificador, latLng);
        //getInfo(identificador, latLng);
    });    
    oms.addMarker(marker);*/

    gmarkers.push(marker);
    glabels.push(label);
    marker.bindTo('map', myLayers, data.properties.custom_check);
    google.maps.event.addListener(marker, 'click', function(e) {  // 'spider_click', not plain 'click'
        getInfo(identificador, latLng);
        //getInfo(identificador, latLng);
    });    
    //console.log('admarker:'+data.properties.custom_check);
    bounds.extend(latLng);
    map.fitBounds(bounds);    
}

// tussam-bts
// License: CC0 1.0 Universal

var route = document.getElementById("route").value;

var points = new ol.layer.Vector();

var map = new ol.Map({
    layers: [
        new ol.layer.Tile({
            source: new ol.source.XYZ({
                url: 'http://{1-4}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
            })
        }),
        points
    ],
    target: 'map',
    view: new ol.View({
        center: ol.proj.fromLonLat([-5.986944, 37.377222]),
        zoom: 12
    })
});

function renderPoints(positions) {
    var features = new Array(positions.length);

    positions.forEach(function(pos, i) {
        features[i] = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat(pos)),
        })
    });

    var vectorSource = new ol.source.Vector({
        features: features
    });

    var dotStyle = new ol.style.Style({
        image: new ol.style.Icon(({
            scale: 0.5,
            color: '#FF5050',
            crossOrigin: 'anonymous',
            src: 'https://openlayers.org/en/v4.6.4/examples/data/dot.png'
        }))
    });

    var VectorLayer = new ol.layer.Vector({
        source: vectorSource,
        style: dotStyle
    });

    map.removeLayer(points);
    points = VectorLayer;
    map.addLayer(points);
}

function processPositions(response) {
    var positions = JSON.parse(response);
    renderPoints(positions)
}

function httpGetAsync(url, callback) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200)
            callback(request.responseText);
    }
    request.open("GET", url, true);
    request.send(null);
}

function changeRoute() {
    route = document.getElementById("route").value;
    // Force refresh
    httpGetAsync("http://localhost:8080/" + route, processPositions)
}

setInterval(function() {
    httpGetAsync("http://localhost:8080/" + route, processPositions)
}, 5000);

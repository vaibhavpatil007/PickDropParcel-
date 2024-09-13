// Initialize the map
var map = L.map('map').setView([21.7679,78.8718], 5);  // Default view set to London

// Add OpenStreetMap TileLayer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
}).addTo(map);

// // Add zones (restricted, non-flying, etc.)
// L.circle([51.505, -0.09], { color: 'red', radius: 500, fillOpacity: 0.5 }).addTo(map).bindPopup('Restricted Zone');
// L.circle([51.515, -0.1], { color: 'orange', radius: 300, fillOpacity: 0.5 }).addTo(map).bindPopup('No-Flying Zone');
// L.circle([51.525, -0.08], { color: 'green', radius: 700, fillOpacity: 0.5 }).addTo(map).bindPopup('Green Zone');
// Dynamic zones for India
const redZones = [
    { lat: 28.7041, lng: 77.1025, radius: 1000 },  // Delhi
    { lat: 19.0760, lng: 72.8777, radius: 1200 },  // Mumbai
    { lat: 15.813576, lng: 80.354729, radius: 1200 },  // Mumbai
    { lat: 9.931233, lng: 76.267303, radius: 2000 },
    { lat: 20.716139, lng: 70.918980, radius: 2000 },
    { lat: 20.720073, lng: 70.747318, radius: 2000 },
    { lat: 20.757238, lng: 70.661831, radius: 2000 },
    { lat: 20.835831, lng: 70.692430, radius: 2000 },
    { lat: 20.920637, lng: 70.508722, radius: 2000 }, 
    { lat: 21.754398, lng: 72.183266, radius: 2000 },  // Mumbai
    { lat: 21.652323, lng: 69.654350, radius: 2000 },
    { lat: 22.468147, lng: 70.004883, radius: 2000 },
    { lat: 23.069624, lng: 72.626495, radius: 2000 },
    { lat: 22.324671, lng: 73.226624, radius: 2000 },
    { lat: 20.958875, lng: 75.627136, radius: 5000 },
    { lat: 20.901154, lng: 75.793806, radius: 5000 },
    { lat: 20.942162, lng: 75.453659, radius: 5000 },
    { lat: 20.118968, lng: 73.922367, radius: 5000 },
    { lat: 20.083180, lng: 73.858852, radius: 5000 },
    { lat: 20.061575, lng: 73.889408, radius: 5000 },
    { lat: 19.988839, lng: 73.796539, radius: 5000 },
    { lat: 20.900753, lng: 74.793849, radius: 200 },
    { lat: 20.927171, lng: 74.739668, radius: 2000 },  //Dhule airport
    { lat: 20.787412, lng: 74.774837, radius: 5000 },
    { lat: 20.748890, lng: 74.899035, radius: 5000 },
    { lat: 21.001349, lng: 75.604134, radius: 5000 },
    { lat: 21.298011, lng: 74.806595, radius: 5000 },
    { lat: 19.864894, lng: 75.392990, radius: 5000 },
    
      // Mumbai

];

const orangeZones = [
    { lat: 13.0827, lng: 80.2707, radius: 900 },  // Chennai
];

const greenZones = [
    { lat: 22.5726, lng: 88.3639, radius: 800 },  // Kolkata
];

// Add zones dynamically
redZones.forEach(zone => {
    L.circle([zone.lat, zone.lng], { color: 'red', radius: zone.radius, fillOpacity: 0.5 })
        .addTo(map)
        .bindPopup('Restricted Zone');
});

orangeZones.forEach(zone => {
    L.circle([zone.lat, zone.lng], { color: 'orange', radius: zone.radius, fillOpacity: 0.5 })
        .addTo(map)
        .bindPopup('No-Flying Zone');
});

greenZones.forEach(zone => {
    L.circle([zone.lat, zone.lng], { color: 'green', radius: zone.radius, fillOpacity: 0.5 })
        .addTo(map)
        .bindPopup('Green Zone');
});

// Variables to keep track of markers and lines
let markers = [];
let polyline;
let markerCount = 1;

// Marker colors based on options
const markerOptions = {
    "takeoff": { color: "green", labelClass: "popup-takeoff" },
    "away": { color: "orange", labelClass: "popup-away" },
    "pickup": { color: "blue", labelClass: "popup-pickup" },
    "dispatch": { color: "purple", labelClass: "popup-dispatch" },
    "return": { color: "red", labelClass: "popup-return" }
};

// Function to add a marker with options and details
document.getElementById('addMarker').addEventListener('click', () => {
    map.on('click', function onMapClick(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;

        const marker = L.marker([lat, lng], { draggable: true }).addTo(map);

        const popupContent = `
            <b>Marker ${markerCount}</b><br>
            Altitude: <input type="number" id="altitude" placeholder="Enter Altitude"><br>
            Speed: <input type="number" id="speed" placeholder="Enter Speed"><br>
            <select id="markerOption">
                <option value="takeoff">Takeoff</option>
                <option value="WayPoint">Away</option>
                <option value="pickup">Pickup</option>
                <option value="dispatch">Dispatch</option>
                <option value="return">Return</option>
            </select><br>
            <button id="saveMarker">Save</button>
        `;

        marker.bindPopup(popupContent).openPopup();

        markers.push({ marker: marker, id: markerCount });
        markerCount++;

        map.off('click', onMapClick);  // Disable click after one marker

        // Draw line between markers
        if (markers.length > 1) {
            const latlngs = markers.map(m => m.marker.getLatLng());
            if (polyline) map.removeLayer(polyline);  // Remove old line
            polyline = L.polyline(latlngs, { color: 'blue' }).addTo(map);  // Draw line
        }
    });
});

// Save the marker options when user clicks save
map.on('popupopen', (e) => {
    document.getElementById('saveMarker').addEventListener('click', function () {
        const markerOption = document.getElementById('markerOption').value;
        const altitude = document.getElementById('altitude').value;
        const speed = document.getElementById('speed').value;

        const currentMarker = markers.find(m => m.marker._leaflet_id === e.popup._source._leaflet_id);
        
        if (currentMarker) {
            currentMarker.option = markerOption;
            currentMarker.altitude = altitude;
            currentMarker.speed = speed;

            e.popup.setContent(`
                <div class="popup-label ${markerOptions[markerOption].labelClass}">
                    ${markerOption.toUpperCase()} <br> Altitude: ${altitude}m <br> Speed: ${speed}m/s
                </div>
            `);
        }

        e.popup.update();
    });
});

// Function to focus the map on a given latitude and longitude
document.getElementById('focusMap').addEventListener('click', () => {
    const lat = document.getElementById('latInput').value;
    const lng = document.getElementById('lngInput').value;
    const focus_marker = L.marker([lat, lng], { draggable: true })
            .addTo(map)
            .bindPopup('<b>Marker</b>')
            .openPopup();
            console.log(pickupMarker)

    map.setView([lat, lng], 13);
});

// Fly drone animation (this is a simulation with drone icon)
document.getElementById('flyDrone').addEventListener('click', () => {
    if (!polyline) {
        alert('Please set markers and route first!');
        return;
    }

    const droneIcon = L.icon({
        iconUrl: '/static/fly_drone.svg',  // replace with actual drone icon path
        iconSize: [50, 50]
    });

    let latlngs = polyline.getLatLngs();
    let index = 0;
    
    let drone = L.marker(latlngs[index], { icon: droneIcon }).addTo(map);

    function animateDrone() {
        if (index < latlngs.length - 1) {
            index++;
            drone.setLatLng(latlngs[index]);
            setTimeout(animateDrone, 2000);  // Adjust speed of animation here
        }
    }
    animateDrone();
});

// Handle marker connections using AJAX
document.getElementById('connectMarker').addEventListener('click', () => {
    
    const orderId = document.getElementById('connectMarker').getAttribute('data-order-id');
    fetch(`/api/get-coordinates/${orderId}`)
    // fetch('/api/get-coordinates/1')
    .then(response => response.json())
    .then(data => {
        const pickupLat = data.pickup_latitude;
        const pickupLng = data.pickup_longitude;
        const dropoffLat = data.dropoff_latitude;
        const dropoffLng = data.dropoff_longitude;

        // Add Pickup Marker
        const pickupMarker = L.marker([pickupLat, pickupLng], { draggable: true })
            .addTo(map)
            .bindPopup('<b>Pickup Location</b>')
            .openPopup();
            console.log(pickupMarker)

        // Add Dropoff Marker
        const dropoffMarker = L.marker([dropoffLat, dropoffLng], { draggable: true })
            .addTo(map)
            .bindPopup('<b>Dropoff Location</b>')
            .openPopup();
            console.log(dropoffMarker)

        // Connect markers with a line
        const latlngs = [[pickupLat, pickupLng], [dropoffLat, dropoffLng]];
        L.polyline(latlngs, { color: 'blue' }).addTo(map);
    })
    .catch(error => {
        console.error('Error fetching coordinates:', error);
    });
});

// Basic Script to simulate changing metrics
let totalFlights = 1020;
let totalDeliveries = 950;

function updateDashboard() {
    document.querySelector('.kpi:nth-child(1) p').innerText = totalFlights;
    document.querySelector('.kpi:nth-child(2) p').innerText = totalDeliveries;
    totalFlights += 1;
    totalDeliveries += 1;
}

setInterval(updateDashboard, 5000); // Updates every 5 seconds

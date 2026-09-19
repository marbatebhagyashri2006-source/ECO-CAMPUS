// ==============================
// EMISSION FACTORS
// ==============================

const ELECTRICITY_FACTOR = 0.827;

const TRANSPORT_FACTORS = {
    two_wheeler: 0.16,
    car: 0.39,
    bus: 1.93
};

const WASTE_FACTORS = {
    composted: 0.32,
    landfill: 1.29
};


// Store latest result
let currentData = {
    electricity: 0,
    transport: 0,
    waste: 0,
    total: 0
};


// ==============================
// CALCULATE CARBON
// ==============================

function calculateCarbon() {

    const electricity =
        Number(document.getElementById("electricity").value);

    const vehicle =
        document.getElementById("vehicle").value;

    const vehicles =
        Number(document.getElementById("vehicles").value);

    const distance =
        Number(document.getElementById("distance").value);

    const days =
        Number(document.getElementById("days").value);

    const waste =
        Number(document.getElementById("waste").value);

    const treatment =
        document.getElementById("treatment").value;


    // Basic validation

    if (
        electricity <= 0 ||
        vehicles <= 0 ||
        distance <= 0 ||
        days <= 0 ||
        waste < 0
    ) {
        alert("Please enter valid campus data.");
        return;
    }


    // Electricity
    const electricityEmission =
        electricity * 12 * ELECTRICITY_FACTOR;


    // Transportation
    const annualDistance =
        vehicles * distance * days * 12;

    const transportEmission =
        annualDistance * TRANSPORT_FACTORS[vehicle];


    // Waste
    const annualWaste =
        waste * 12;

    const wasteEmission =
        annualWaste * WASTE_FACTORS[treatment];


    // Total
    const total =
        electricityEmission +
        transportEmission +
        wasteEmission;


    currentData = {
        electricity: electricityEmission,
        transport: transportEmission,
        waste: wasteEmission,
        total: total
    };


    displayResults();

    updateSimulation();

    generateRecommendations();

    document.getElementById("dashboard")
        .classList.remove("hidden");

    document.getElementById("simulator")
        .classList.remove("hidden");

    document.getElementById("recommendations")
        .classList.remove("hidden");

    document.getElementById("dashboard")
        .scrollIntoView({
            behavior: "smooth"
        });
}


// ==============================
// DISPLAY RESULTS
// ==============================

function displayResults() {

    const electricity =
        currentData.electricity / 1000;

    const transport =
        currentData.transport / 1000;

    const waste =
        currentData.waste / 1000;

    const total =
        currentData.total / 1000;


    document.getElementById("electricityResult")
        .textContent = electricity.toFixed(2);

    document.getElementById("transportResult")
        .textContent = transport.toFixed(2);

    document.getElementById("wasteResult")
        .textContent = waste.toFixed(2);

    document.getElementById("totalEmission")
        .textContent = total.toFixed(2);


    // Percentage bars

    const electricityPercent =
        (currentData.electricity / currentData.total) * 100;

    const transportPercent =
        (currentData.transport / currentData.total) * 100;

    const wastePercent =
        (currentData.waste / currentData.total) * 100;


    document.getElementById("electricityBar")
        .style.width = electricityPercent + "%";

    document.getElementById("transportBar")
        .style.width = transportPercent + "%";

    document.getElementById("wasteBar")
        .style.width = wastePercent + "%";
}


// ==============================
// WHAT-IF SIMULATOR
// ==============================

function updateSimulation() {

    const reduction =
        Number(document.getElementById("reduction").value);

    document.getElementById("reductionValue")
        .textContent = reduction + "%";


    const current =
        currentData.total / 1000;

    const electricity =
        currentData.electricity / 1000;


    const electricitySaving =
        electricity * (reduction / 100);

    const projected =
        current - electricitySaving;


    document.getElementById("currentFootprint")
        .textContent = current.toFixed(2);

    document.getElementById("projectedFootprint")
        .textContent = projected.toFixed(2);

    document.getElementById("savedEmission")
        .textContent = electricitySaving.toFixed(2);
}


// ==============================
// RECOMMENDATIONS
// ==============================

function generateRecommendations() {

    const list =
        document.getElementById("recommendationList");

    list.innerHTML = "";


    const sources = [
        {
            name: "Electricity",
            value: currentData.electricity,
            icon: "⚡",
            text: "Consider LED lighting, energy-efficient equipment, smart power management and solar energy."
        },
        {
            name: "Transportation",
            value: currentData.transport,
            icon: "🚌",
            text: "Encourage public transport, carpooling, cycling and optimized campus transport."
        },
        {
            name: "Waste",
            value: currentData.waste,
            icon: "🗑️",
            text: "Improve waste segregation, compost organic waste and increase recycling."
        }
    ];


    sources
        .sort((a, b) => b.value - a.value)
        .forEach((source) => {

            const card =
                document.createElement("div");

            card.className =
                "recommendation-card";

            card.innerHTML = `
                <h3>${source.icon} ${source.name}</h3>
                <p>${source.text}</p>
            `;

            list.appendChild(card);
        });
}
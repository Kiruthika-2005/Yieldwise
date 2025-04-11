// Sample data for commodities (Updated)
const commodities = ["Select",
    "Tomato",
    "Potato",
    "Onion",
    "Carrot",
    "Cabbage",
    "Carrot (Local)",
    "Brinjal",
    "Cabbage (Local)",
    "Radish Red",
    "Brinjal Long",
    "Soybean Green",
    "Garlic",
    "Ginger",
    "Peas",
    "Green Peas",
    "Smooth Gourd",
    "Sponge Gourd",
    "Radish White (Local)",
    "Chili",
    "Okra",
    "Squash (Long)",
    "Fenugreek",
    "Green Beans",
    "Jackfruit",
    "Broccoli",
    "Pointed Gourd (Local)",
    "Spinach Leaf",
    "Bamboo Shoot",
    "Sweet Potato",
    "Fenugreek Leaf",
    "Cauliflower (Local)",
    "Jack Fruit",
    "Leek",
    "Mustard Leaf",
    "Brinjal Round",
    "Broad Leaf Mustard",
    "Mushroom (Kanya)",
    "Christophine",
    "Asparagus",
    "Turnip A",
    "Brussels Sprout",
    "Chilli Green (Machhe)",
    "Mustard Greens",
    "Garlic Dry Chinese",
    "Mango (Maldah)",
    "Garlic Dry Nepali",
    "Sugarcane",
    "Chilli Green (Bullet)",
    "Rhubarb",
    "French Bean (Hybrid)"
];


// Function to populate the select element with commodities
function populateSelectOptions() {
    const commoditySelect = document.getElementById('commodity');
    commoditySelect.innerHTML = ""; // Clear previous options

    // Populate dropdown with commodities
    commodities.forEach(commodity => {
        const option = document.createElement('option');
        option.value = commodity.toLowerCase(); // Ensure value is lowercase for consistency
        option.textContent = commodity;
        commoditySelect.appendChild(option);
    });
}

// Function to fetch commodities from Flask backend
function loadCommodities() {
    fetch('http://127.0.0.1:5000/get-commodities')
        .then(response => response.json())
        .then(data => {
            const commoditySelect = document.getElementById('commodity');
            commoditySelect.innerHTML = ""; // Clear previous options

            // Populate dropdown with commodities from backend
            data.commodities.forEach(commodity => {
                const option = document.createElement('option');
                option.value = commodity.toLowerCase(); // Ensure value is lowercase for consistency
                option.textContent = commodity;
                commoditySelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching commodities:', error);
            alert("Failed to load commodities. Please check your backend.");
        });
}

// Function to fetch predicted price
function fetchPrediction() {
    const selectedCommodity = document.getElementById('commodity').value;
    const selectedState = document.getElementById('state').value; // Get selected state

    if (!selectedCommodity || !selectedState) {
        alert("Please select both a commodity and a state.");
        return;
    }

    fetch(`http://127.0.0.1:5000/get-prediction/${selectedCommodity}/${selectedState}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('predictedPrice').textContent = 
                `Predicted Price for ${data.commodity} in ${data.state}: ${data.predicted_price}`;
            document.getElementById('outputSection').style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching prediction:', error);
            // alert("Failed to fetch prediction. Please try again.");
        });
}

// Attach event listener to "Go" button
document.getElementById('goButton').addEventListener('click', fetchPrediction);

// Load commodities when the page loads
window.onload = () => {
    populateSelectOptions(); // Populate with static list first
    loadCommodities();       // Then try fetching from backend
};

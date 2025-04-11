document.getElementById('submitMonthly').addEventListener('click', function () {
    const selectedCommodity = document.getElementById('monthlyCommodity').value;

    if (selectedCommodity === "Select Commodity") {
        alert("Please select a valid commodity.");
        return;
    }

    // Construct the correct path to the saved graph PNG
    const imagePath = `vegetable_models/${selectedCommodity}_prediction_graph.png`;

    // Check if the image exists
    checkImage(imagePath, function (exists) {
        if (exists) {
            showImage(imagePath);
        } else {
            alert(`Graph not found for ${selectedCommodity}. Please make sure the graph is saved correctly.`);
            document.getElementById('graphSection').style.display = 'none';
        }
    });
});

// Reset functionality
document.getElementById('resetMonthly').addEventListener('click', function () {
    document.getElementById('monthlyCommodity').value = "Select Commodity";
    document.getElementById('graphSection').style.display = 'none';
});

// Function to check if the image exists
function checkImage(imagePath, callback) {
    const img = new Image();
    img.onload = function () {
        callback(true);
    };
    img.onerror = function () {
        callback(false);
    };
    img.src = imagePath;
}

// Function to show the graph image dynamically
function showImage(imagePath) {
    const graphSection = document.getElementById('graphSection');
    graphSection.innerHTML = `
        <h2 class="text-2xl font-bold text-center mb-4">Monthly Price Trend</h2>
        <img src="${imagePath}" alt="Monthly Price Trend" class="w-full h-auto mx-auto border rounded-lg shadow-md">
    `;
    graphSection.style.display = 'block';
}

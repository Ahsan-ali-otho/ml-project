let predictionsChart; // Declare predictionsChart globally

async function fetchPredictions() {
  const predictionsDiv = document.getElementById("predictions");
  predictionsDiv.innerHTML = `
        <p>Loading predictions...</p>
        <div class="spinner-border" role="status">
            <span class="sr-only">Loading...</span>
        </div>`; // Loading message with spinner for better user experience

  try {
    const response = await fetch("http://127.0.0.1:5000/predict");

    if (!response.ok) {
      throw new Error(
        "Network response was not ok. Status: " + response.status
      );
    }

    const data = await response.json();

    // Validate the response data structure
    if (!data.predictions || !Array.isArray(data.predictions)) {
      throw new Error(
        "Invalid data format: predictions missing or not an array."
      );
    }

    displayPredictions(data);
  } catch (error) {
    console.error("Error fetching predictions:", error);
    predictionsDiv.innerHTML = `
            <p>Error fetching predictions: ${error.message}. Please try again later.</p>`; // User-friendly error message
  }
}

function displayPredictions(data) {
  const predictionsDiv = document.getElementById("predictions");
  predictionsDiv.innerHTML = ""; // Clear loading message

  // Extract dates and prices
  const dates = data.predictions.map((pred) => pred.Date);
  const prices = data.predictions.map((pred) => pred["Predicted Price"]); // Corrected key

  // Create the chart
  const ctx = document.getElementById("predictionsChart").getContext("2d");

  // Destroy existing chart if it exists to avoid conflicts
  if (predictionsChart) {
    predictionsChart.destroy();
  }

  predictionsChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: dates,
      datasets: [
        {
          label: "Predicted Prices",
          data: prices,
          borderColor: "rgba(75, 192, 192, 1)",
          fill: false,
          tension: 0.1, // Smooth lines
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: false, // Changed to false for better visual representation of prices
          title: {
            display: true,
            text: "Price ($)",
          },
        },
        x: {
          title: {
            display: true,
            text: "Date",
          },
        },
      },
      plugins: {
        legend: {
          position: "top", // Positioning the legend at the top
        },
        tooltip: {
          mode: "index", // Tooltip mode for better readability
          intersect: false,
        },
      },
    },
  });

  // Display advice and error metrics
  predictionsDiv.innerHTML += `<h2>Advice: ${data.advice}</h2>`;
  predictionsDiv.innerHTML += `<h3>Absolute Mean of Predictions: ${data.absolute_mean.toFixed(
    2
  )}</h3>`;
  predictionsDiv.innerHTML += `<h3>Mean Absolute Error: ${data.mae.toFixed(
    2
  )}</h3>`;
  predictionsDiv.innerHTML += `<h3>Mean Squared Error: ${data.mse.toFixed(
    2
  )}</h3>`;
  predictionsDiv.innerHTML += `<h3>Target Price: ${data.target_price}</h3>`;

  // Create and display the table
  const table = document.createElement("table");
  table.style.width = "100%";
  table.style.borderCollapse = "collapse";
  table.innerHTML = `
        <thead>
            <tr>
                <th>Date</th>
                <th>Predicted Price ($)</th>
            </tr>
        </thead>
        <tbody>
            ${data.predictions
              .map(
                (pred) => `
                <tr>
                    <td>${pred.Date}</td>
                    <td>${pred["Predicted Price"].toFixed(
                      2
                    )}</td> <!-- Ensure prices are formatted -->
                </tr>
            `
              )
              .join("")}
        </tbody>
    `;
  predictionsDiv.appendChild(table);
}

// Call the fetch function when the page loads
window.onload = fetchPredictions;

// Handle window resize for better responsiveness
window.addEventListener("resize", () => {
  if (predictionsChart) {
    predictionsChart.resize();
  }
});

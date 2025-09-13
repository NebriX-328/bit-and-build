document.addEventListener("DOMContentLoaded", () => {
  const projectsDiv = document.getElementById("ngo-projects");
  const chartCanvas = document.getElementById("ngoFundsChart");

  // Example NGO projects
  const projects = [
    {
      name: "Community Health Drive",
      status: "Completed",
      fundsUsed: 80000,
      upload: true,
    },
    {
      name: "Rural Education Program",
      status: "Ongoing",
      fundsUsed: 60000,
      upload: false,
    },
    {
      name: "Environmental Awareness Campaign",
      status: "Upcoming",
      fundsUsed: 40000,
      upload: false,
    },
    {
      name: "Women Empowerment Initiative",
      status: "Completed",
      fundsUsed: 70000,
      upload: true,
    },
  ];

  // Render project list
  projectsDiv.innerHTML = projects
    .map(
      (p) => `
      <div class="project">
        <h3>${p.name}</h3>
        <p>Status: <strong>${p.status}</strong></p>
        <p>Funds Allocated: ₹${p.fundsUsed.toLocaleString()}</p>
        ${
          p.upload
            ? `
          <label>Upload Invoice:</label>
          <input type="file" accept=".pdf,.jpg,.png"><br>
          <label>Upload Image:</label>
          <input type="file" accept="image/*"><br>
        `
            : ""
        }
      </div>
    `
    )
    .join("");

  // Chart.js Pie Chart
  if (chartCanvas) {
    const ctx = chartCanvas.getContext("2d");
    new Chart(ctx, {
      type: "pie",
      data: {
        labels: projects.map((p) => p.name),
        datasets: [
          {
            data: projects.map((p) => p.fundsUsed),
            backgroundColor: ["#E91E63", "#9C27B0", "#FF9800", "#4CAF50"],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "bottom" },
        },
      },
    });
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const projectsDiv = document.getElementById("government-projects");
  const chartCanvas = document.getElementById("govFundsChart");

  // Example Government projects
  const projects = [
    {
      name: "Smart City Development",
      status: "Ongoing",
      fundsUsed: 7500000,
      upload: false,
    },
    {
      name: "Public Health Scheme",
      status: "Completed",
      fundsUsed: 5000000,
      upload: true,
    },
    {
      name: "National Education Program",
      status: "Upcoming",
      fundsUsed: 3000000,
      upload: false,
    },
    {
      name: "Renewable Energy Initiative",
      status: "Completed",
      fundsUsed: 4500000,
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
            backgroundColor: ["#1a237e", "#3949ab", "#5c6bc0", "#9fa8da"],
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

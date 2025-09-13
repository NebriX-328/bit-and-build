

document.addEventListener("DOMContentLoaded", () => {
  const projectsDiv = document.getElementById("institution-projects");
  const chartCanvas = document.getElementById("instFundsChart");

  // Example Institution projects
  const projects = [
    {
      name: "Advanced Lab Equipment Purchase",
      status: "Completed",
      fundsUsed: 200000,
      upload: true,
    },
    {
      name: "Scholarship Program 2024",
      status: "Ongoing",
      fundsUsed: 150000,
      upload: false,
    },
    {
      name: "AI & Robotics Research Center",
      status: "Upcoming",
      fundsUsed: 100000,
      upload: false,
    },
    {
      name: "Library Digitalization Project",
      status: "Completed",
      fundsUsed: 120000,
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
            backgroundColor: ["#4CAF50", "#2196F3", "#FFC107", "#FF5722"],
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

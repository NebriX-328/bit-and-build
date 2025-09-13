document.addEventListener("DOMContentLoaded", () => {
  const fundsSection = document.getElementById("funds-section");
  const projectsDiv = document.getElementById("funds-projects");
  const chartCanvas = document.getElementById("fundsChart");

  if (!fundsSection) return; // exit if section not found

  // Example project data for an institution
  const projects = [
    {
      name: "Lab Equipment Purchase",
      status: "Completed",
      fundsUsed: 50000,
      upload: true,
    },
    {
      name: "Scholarship Program 2024",
      status: "Ongoing",
      fundsUsed: 30000,
      upload: false,
    },
    {
      name: "Green Energy Research Lab",
      status: "Upcoming",
      fundsUsed: 20000,
      upload: false,
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

  // Fund Utilization Chart (Pie)
  if (chartCanvas) {
    const ctx = chartCanvas.getContext("2d");
    new Chart(ctx, {
      type: "pie",
      data: {
        labels: projects.map((p) => p.name),
        datasets: [
          {
            data: projects.map((p) => p.fundsUsed),
            backgroundColor: ["#4CAF50", "#2196F3", "#FFC107"],
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

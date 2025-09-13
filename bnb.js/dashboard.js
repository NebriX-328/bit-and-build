window.onload = function () {
  const storedData = localStorage.getItem("loginDetails");
  const detailsDiv = document.getElementById("details");

  if (storedData) {
    const { username, email, role } = JSON.parse(storedData);

    // Show login details
    detailsDiv.innerHTML = `
      <p><strong>Username:</strong> ${username}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Role:</strong> ${role}</p>
    `;

    // If role = Institution, show projects & funds
    if (role.toLowerCase() === "institution") {
      document.getElementById("institution-projects").style.display = "block";
      document.getElementById("funds-section").style.display = "block";

      // Example institution projects
      const projects = [
        { name: "Lab Equipment Purchase", status: "Completed", upload: true },
        { name: "Scholarship Program 2024", status: "Ongoing", upload: false },
        { name: "Green Energy Research Lab", status: "Completed", upload: true },
      ];

      const projectListDiv = document.getElementById("projects-list");
      projectListDiv.innerHTML = projects
        .map(
          (p, i) => `
          <div class="project">
            <h3>${p.name}</h3>
            <p>Status: <strong>${p.status}</strong></p>
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

      // Example Fund Flow Data
      const ctx = document.getElementById("fundChart").getContext("2d");
      new Chart(ctx, {
        type: "pie",
        data: {
          labels: ["Lab Equipment", "Scholarships", "Research"],
          datasets: [
            {
              data: [50000, 30000, 20000],
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
  } else {
    detailsDiv.innerHTML =
      "<p>No login details found. Please log in again.</p>";
  }
};

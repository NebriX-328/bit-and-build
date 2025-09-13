document.getElementById("loginForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const role = document.getElementById("role").value;

  // Save login details
  localStorage.setItem("loginDetails", JSON.stringify({ username, email, role }));

  // Redirect to dashboard
  window.location.href = "dashboard.html";
});

// Sample user data
var user = {
    username: "john_doe",
    email: "john@example.com",
    name: "John Doe",
    gender: "",
    role: ""
  };

  var originalUserData = {}; // Store original user data

  // Function to display the user profile
  function showProfile() {
    document.getElementById("profileSection").style.display = "block";
    document.getElementById("username").textContent = user.username;
    document.getElementById("email").textContent = user.email;
    document.getElementById("name").textContent = user.name;
    document.getElementById("gender").textContent = user.gender;
    document.getElementById("role").textContent = user.role;
  }

  // Function to handle user photo click and display the profile
  function displayProfile() {
    showProfile();
    document.getElementById("profileSection").style.display = "none";
  }

  // Function to enable profile editing
  function enableEdit() {
    // Store the original user data before editing
    originalUserData = {
      username: document.getElementById("username").textContent,
      email: document.getElementById("email").textContent,
      name: document.getElementById("name").textContent,
      gender: document.getElementById("gender").textContent,
      role: document.getElementById("role").textContent
    };

    // Enable input fields for editing
    document.getElementById("username").style.display = "none";
    document.getElementById("email").style.display = "none";
    document.getElementById("name").style.display = "none";
    document.getElementById("gender").style.display = "none";
    document.getElementById("role").style.display = "none";
    document.getElementById("usernameInput").value = originalUserData.username;
    document.getElementById("emailInput").value = originalUserData.email;
    document.getElementById("nameInput").value = originalUserData.name;
    document.getElementById("genderInput").value = originalUserData.gender;
    document.getElementById("roleInput").value = originalUserData.role;
    document.getElementById("usernameInput").style.display = "block";
    document.getElementById("emailInput").style.display = "block";
    document.getElementById("nameInput").style.display = "block";
    document.getElementById("genderInput").style.display = "block";
    document.getElementById("roleInput").style.display = "block";

    // Switch to edit mode
    document.getElementById("editButton").style.display = "none";
    document.querySelector(".profile").classList.add("edit-mode");
    document.querySelector(".edit-buttons").style.display = "block";
  }

  // Function to save profile changes
  function saveProfile() {
    // Get updated user data
    var updatedUserData = {
      username: document.getElementById("usernameInput").value,
      email: document.getElementById("emailInput").value,
      name: document.getElementById("nameInput").value,
      gender: document.getElementById("genderInput").value,
      role: document.getElementById("roleInput").value
    };

    // Perform save operation here using AJAX or fetch API
    // Example: make a request to the server-side endpoint to update the user profile with the updatedUserData
    // Handle the response to determine if the save was successful

    // After saving, update the user object with the updatedUserData
    user = updatedUserData;

    // Disable input fields for editing
    document.getElementById("username").style.display = "block";
    document.getElementById("email").style.display = "block";
    document.getElementById("name").style.display = "block";
    document.getElementById("gender").style.display = "block";
    document.getElementById("role").style.display = "block";
    document.getElementById("usernameInput").style.display = "none";
    document.getElementById("emailInput").style.display = "none";
    document.getElementById("nameInput").style.display = "none";
    document.getElementById("genderInput").style.display = "none";
    document.getElementById("roleInput").style.display = "none";

    // Update the displayed user data
    document.getElementById("username").textContent = user.username;
    document.getElementById("email").textContent = user.email;
    document.getElementById("name").textContent = user.name;
    document.getElementById("gender").textContent = user.gender;
    document.getElementById("role").textContent = user.role;

    // Switch back to view mode
    document.querySelector(".profile").classList.remove("edit-mode");
    document.querySelector(".edit-buttons").style.display = "none";
    document.getElementById("editButton").style.display = "block";
  }

  // Function to cancel profile changes
  function cancelEdit() {
    // Restore the original user data
    document.getElementById("username").textContent = originalUserData.username;
    document.getElementById("email").textContent = originalUserData.email;
    document.getElementById("name").textContent = originalUserData.name;
    document.getElementById("gender").textContent = originalUserData.gender;
    document.getElementById("role").textContent = originalUserData.role;

    // Disable input fields for editing
    document.getElementById("username").style.display = "block";
    document.getElementById("email").style.display = "block";
    document.getElementById("name").style.display = "block";
    document.getElementById("gender").style.display = "block";
    document.getElementById("role").style.display = "block";
    document.getElementById("usernameInput").style.display = "none";
    document.getElementById("emailInput").style.display = "none";
    document.getElementById("nameInput").style.display = "none";
    document.getElementById("genderInput").style.display = "none";
    document.getElementById("roleInput").style.display = "none";

    // Switch back to view mode
    document.querySelector(".profile").classList.remove("edit-mode");
    document.querySelector(".edit-buttons").style.display = "none";
    document.getElementById("editButton").style.display = "block";
  }

  // Add event listener to the edit button click
  document.getElementById("editButton").addEventListener("click", enableEdit);

  // Add event listener to the save button click
  document.getElementById("saveButton").addEventListener("click", saveProfile);

  // Add event listener to the cancel button click
  document.getElementById("cancelButton").addEventListener("click", cancelEdit);
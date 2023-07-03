document.getElementById('signup').addEventListener('click', function(e) {
    e.preventDefault(); // Prevent default form submission behavior

    // Get form input values
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var gender = document.getElementById('gender').value;
    var gender = document.getElementById('role').value;

    // Create an object with the form data
    var formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("gender", gender);
    formData.append("role", role);

    // Make a POST request to the API endpoint
    fetch('http://127.0.0.1:5001/api/v1/register', {
      method: 'POST',
      body: formData
    })
    .then(function(response) {
      if (response.ok) {
        // Successful login, redirect to home page
        window.location.href = '/';
      } else {
        // Failed login, display error message
        alert('Login failed. Please check your credentials.');
      }
    })
    .catch(function(error) {
      console.error('Error:', error);
      alert('An error occurred during login.');
    });
  });
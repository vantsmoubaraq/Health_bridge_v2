document.getElementById('signin').addEventListener('click', function(e) {
    e.preventDefault(); // Prevent default form submission behavior

    // Get form input values
    var email = document.getElementById('email2').value;
    var password = document.getElementById('password2').value;

    // Create an object with the form data
    var formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);

    // Make a POST request to the API endpoint
    fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      body: formData
    })
  });
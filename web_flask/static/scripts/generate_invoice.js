const send = document.getElementById("send");
var patient = window.location.pathname.split('/')[3];

send.addEventListener("click", () => {
    const prescription_id = document.getElementById("p_id").textContent;
    fetch(`http://127.0.0.1:5001/api/v1/prescription_invoice/${prescription_id}`, {
        method: "POST",
    }).then(
        (response) => response.json()
    ).then((data) => {
        console.table(data);
        window.location.href = '/invoices/' + patient;
        function showFlashMessage(message, duration) {
        const flashMessage = document.getElementById('flashMessage');
        
        // Create a new message element
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        
        // Append the message element to the flash message container
        flashMessage.appendChild(messageElement);
        
        // Set a timer to remove the message after the specified duration
        setTimeout(function() {
            flashMessage.removeChild(messageElement);
        }, duration);
        }
        
        // Example usage:
        showFlashMessage('Invoice Successfully Generated!', 3000); // Display success message for 3 seconds
    }).catch(
        (error) => {
            console.log(error);
        }
    )
});


//Delete prescription
document.addEventListener('DOMContentLoaded', function() {
    var actionButton = document.getElementById('action');
    actionButton.addEventListener('click', function(event) {
        var id = document.getElementById("p_id").textContent;
        var route = `http://127.0.0.1:5001/api/v1/prescription/${id}`;
        var patient_id = window.location.pathname.split('/')[3];
        
        fetch(route, {
            method: 'DELETE'
        })
        .then(function(response) {
            if (response.ok) {
                console.log('Deleted Successfully');
                window.location.href = '/prescriptions/' + patient_id;
            } else {
                throw new Error('Error: ' + response.status);
            }
        })
        .catch(function(error) {
            console.log(error);
            console.log(id);
        });
    });
});

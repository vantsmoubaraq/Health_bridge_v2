const send = document.getElementById("send");

send.addEventListener("click", () => {
    const prescription_id = document.getElementById("p_id").textContent;
    fetch(`http://127.0.0.1:5001/api/v1//prescription_invoice/${prescription_id}`, {
        method: "POST",
    }).then(
        (response) => response.json()
    ).then((data) => {
        console.table(data);
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
        showFlashMessage('Action completed successfully!', 3000); // Display success message for 3 seconds
    }).catch(
        (error) => {
            console.log(error);
        }
    )
})
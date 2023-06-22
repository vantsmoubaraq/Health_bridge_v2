const submitButton = document.getElementById('btn');
submitButton.addEventListener('click', (event) => {
    event.preventDefault();
    const form = document.getElementById('myForm');
    const formData = new FormData(form);

        const data = {};
                for (const [key, value] of formData.entries()) {
        data[key] = value;
         }

    const requestOptions = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'}
    };

    const id = window.location.pathname.split('/')[2]


    fetch('http://127.0.0.1:5001/api/v1/payments/' + id, requestOptions)
        .then(response => response.json())
        .then(data => {
                        console.log(data);
                        const my_id = data.id;
                       window.location.href = `/all_payments/${id}`;
                })
        .catch(error => console.error(error));
});

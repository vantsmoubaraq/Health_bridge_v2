//add drug to patient
const names = document.querySelectorAll('.card');

names.forEach(name => {
    name.addEventListener('click', (event)=>{
        const patientId = window.location.pathname.split('/')[2];
        const drugId =  name.querySelector("#drug_id").textContent
        const requestOptions = {
            method: 'POST',
        }

        console.log(patientId);
        console.log(drugId);

        fetch(`http://127.0.0.1:5001/api/v1/patient/${patientId}/drug/${drugId}`, requestOptions).then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Request failed!');
        }).then(data => {
            console.log(data);
            window.location.href = "/prescriptions/" + patientId;
        }).catch(error => { 
            console.log(error);
        });
    });
});

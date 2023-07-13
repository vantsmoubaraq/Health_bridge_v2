const drugs = document.getElementById("drugs");
const formData = new FormData();
var drug_Id;
drug_Id = drugs.value;
console.log(drug_Id);
formData.append("drug_id", drug_Id);
var drug_name = drugs.options[drugs.selectedIndex].textContent;

drugs.addEventListener("change", function() {
    drug_Id = drugs.value;
    const selectedIndex = drugs.selectedIndex;
    drug_name = drugs.options[selectedIndex].textContent;  
    console.log(drug_Id);
    formData.delete("drug_id");
    formData.append("drug_id", drug_Id);
});

//edit prescribed_drug
btn.addEventListener("click", (event) => {
    event.preventDefault();
    const dose = document.getElementById("dose").value;
    const frequency = document.getElementById("frequency").value;
    const days = document.getElementById("days").value;
    const patient_id = window.location.pathname.split('/')[4];
    const prescription_id = window.location.pathname.split('/')[3];
    const prescribed_drug_id = window.location.pathname.split('/')[2];

    formData.append("dosage", dose);
    formData.append("frequency", frequency);
    formData.append("days", days);
    formData.append("drug_id", drug_Id);
    
    const url = `http://127.0.0.1:5001/api/v1/prescribed_drug/${prescribed_drug_id}`
    const data = {
        method: "PUT",
        body: formData,
    }

    fetch(url, data).then((response) => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error: ' + response.status);
        }
    })
    .then((data) => {
        console.log(data);
        window.location.href=`/prescriptions_edit/${prescription_id}/${patient_id}`
    })
    .catch((error) => {
        console.log(error);
    });

});
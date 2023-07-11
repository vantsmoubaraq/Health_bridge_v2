const save = document.getElementById("save")
const drugs = document.getElementById("drugs");
const formData = new FormData();
var drug_Id;
drug_Id = drugs.value;
formData.append("drug_id", drug_Id);

drugs.addEventListener("change", function() {
    drug_Id = drugs.value;    
    console.log(drug_Id);
    formData.delete("drug_id");
    formData.append("drug_id", drug_Id);
});

save.addEventListener("click", () => {
    const dose = document.getElementById("dose").value;
    const frequency = document.getElementById("Frequency").value;
    const days = document.getElementById("days").value;
    const prescription_id = document.getElementById("p_id").textContent;
    console.log(prescription_id)

    formData.append("dosage", dose);
    formData.append("frequency", frequency);
    formData.append("days", days);
    formData.append("prescription_id", prescription_id);
    
    const url = `http://127.0.0.1:5001/api/v1/prescribe_drug/${prescription_id}`
    const data = {
        method: "POST",
        body: formData,
    }

    fetch(url, data).then(
        (response) => response.json()
    ).then(
        (data) => {console.log(data);}
    ).catch(
        (error) => {console.log(error);}
    );

})
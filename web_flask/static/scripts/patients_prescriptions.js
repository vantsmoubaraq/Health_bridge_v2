const save = document.getElementById("save")
const drugs = document.getElementById("drugs");
const formData = new FormData();
var drug_Id;
drug_Id = drugs.value;
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

    fetch(url, data).then((response) => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error: ' + response.status);
        }
    })
    .then((data) => {
        console.log(data);
        addRow(dose, frequency, days, drug_name);
        resetForm();
    })
    .catch((error) => {
        console.log(error);
    });

});

function addRow(dose, frequency, days, drug_name) {
    let table = document.getElementById("medicines");
    let row = table.insertRow(1); // Insert at the second position (index 1)
  
    // Create table cells
    let cell1 = row.insertCell(0);
    let cell3 = row.insertCell(1);
    let cell6 = row.insertCell(2);
    let cell8 = row.insertCell(3);
    let cell9 = row.insertCell(4);
  
    // Add data to cells
    cell1.textContent = drug_name;
    cell3.textContent = dose + " mg/mL";
    cell6.textContent = frequency + " times";
    cell8.textContent = days + " days";
    cell9.textContent = getCurrentTime();
  }

  document.addEventListener('click', function(event) {
    var target = event.target;
    if (!cardPopup.contains(target) && target !== addButton && target !== save) {
      cardPopup.classList.add('hidden');
    }
  });

  function getCurrentTime() {
    const currentTime = new Date();
    const utcTime = currentTime.toISOString().replace("T", " ").replace("Z", "");
    return utcTime;
}


function resetForm() {
    const form = document.getElementById('yourFormId');
    form.reset();
}


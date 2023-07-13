const addDrugButton = document.getElementById('addDrugButton');
const drugContainer = document.getElementById('drugContainer');
const submitButton = document.getElementById('submitButton');

addDrugButton.addEventListener('click', () => {
    const drugRow = document.createElement('div');
    drugRow.className = 'drug-row';

    const drugNameLabel = document.createElement('label');
    drugNameLabel.textContent = 'Drug Name:';
    const drugNameInput = document.createElement('input');
    drugNameInput.type = 'text';
    drugNameInput.className = 'drugName';
    drugNameInput.name = 'drugName';
    drugNameInput.required = true;

    const quantityLabel = document.createElement('label');
    quantityLabel.textContent = 'Quantity:';
    const quantityInput = document.createElement('input');
    quantityInput.type = 'number';
    quantityInput.className = 'quantity';
    quantityInput.name = 'quantity';
    quantityInput.required = true;

    const priceLabel = document.createElement('label');
    priceLabel.textContent = 'Price:';
    const priceInput = document.createElement('input');
    priceInput.type = 'number';
    priceInput.className = 'price';
    priceInput.name = 'price';
    priceInput.required = true;

    drugRow.appendChild(drugNameLabel);
    drugRow.appendChild(drugNameInput);
    drugRow.appendChild(quantityLabel);
    drugRow.appendChild(quantityInput);
    drugRow.appendChild(priceLabel);
    drugRow.appendChild(priceInput);

    drugContainer.appendChild(drugRow);
});

submitButton.addEventListener('click', (event) => {
    event.preventDefault();

    const vendorName = document.getElementById('vendorName').value;

    const drugs = [];
    const drugRows = document.getElementsByClassName('drug-row');
    for (let i = 0; i < drugRows.length; i++) {
        const drugName = drugRows[i].querySelector('.drugName').value;
        const quantity = drugRows[i].querySelector('.quantity').value;
        const price = drugRows[i].querySelector('.price').value;

        const drug = {
            name: drugName,
            quantity: quantity,
            price: price
        };

        drugs.push(drug);
    }

    const data = {
        vendor_name: vendorName,
        drugs: drugs
    };

    const requestOptions = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' }
    };

    fetch('http://127.0.0.1:5001/api/v1/procurements', requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            window.location.href = '/procurements';
        })
        .catch(error => console.error(error));
});
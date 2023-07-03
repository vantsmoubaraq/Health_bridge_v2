document.getElementById("btns").addEventListener(
'click', function(event) {
event.preventDefault();
const form = document.getElementById("myForms");
const formdata = new FormData(form);

const data = {};
for (const [key, value] of formdata.entries()){
  data[key] = value;
}

const id = window.location.pathname.split("/")[2]

const submit_data = {
method: 'PUT',
body: JSON.stringify(data),
headers: {'Content-Type': 'application/json'}
};

const url = 'http://127.0.0.1:5001/api/v1/service/' + id;

fetch( url, submit_data
).then(response => response.json()).then(
data => {console.log(data);
window.location.href = `/single_service/${id}`;}
).catch(error => console.error(error))
});

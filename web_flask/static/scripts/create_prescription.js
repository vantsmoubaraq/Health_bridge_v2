const create = document.getElementById("create");

create.addEventListener("click", () => {
    const id = window.location.pathname.split("/")[2]
    fetch(`http://127.0.0.1:5001/api/v1/prescriptions/${id}`, {
        method: "POST",
    }).then(
        (response) => response.json()
    ).then((data) => {
        console.table(data);
        window.location.href = `/prescriptions_page/${id}`;
    }).catch(
        (error) => {
            console.log(error);
        }
    )
})
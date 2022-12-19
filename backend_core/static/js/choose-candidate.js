function sendJson(userId) {
    let xhr = new XMLHttpRequest();
    let url = "";
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    let data = JSON.stringify({"candidate_id": userId});
    xhr.send(data);
}

let hireBtns = document.querySelectorAll(".hire-button");
hireBtns.forEach(btn => {
    btn.onclick = function(e) {
        e.preventDefault();
        sendJson(btn.id);

        const candDiv = document.querySelector("#candidate-list");
        candDiv.remove();
    }
});

let cancelBtn = document.querySelector("#cancel-btn");
cancelBtn.onclick = function(e) {
    e.preventDefault();
    dataId = cancelBtn.getAttribute('data-id');
    cancelBtn.classList.add('d-none');

    const confirm = document.querySelector("#cancel-confirmation");
    confirm.classList.remove('d-none');

    const confirmBtn = document.querySelector("#confirm-btn");
    const discardBtn = document.querySelector("#discard-btn");

    confirmBtn.onclick = function() {
        sendJson(dataId);
        const agentDiv = document.querySelector("#hired-agent");
        agentDiv.remove();
    }

    discardBtn.onclick = function() {
        confirm.classList.add('d-none');
        cancelBtn.classList.remove('d-none');
    }
}

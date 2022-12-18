let hireBtns = document.querySelectorAll(".hire-button");

hireBtns.forEach(btn => {
    btn.onclick = function(e) {
        e.preventDefault();
        console.log("CLICK!" + btn.id);

        let xhr = new XMLHttpRequest();
        let url = "";
        const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("X-CSRFToken", csrfToken);

        let data = JSON.stringify({"candidate_id": btn.id});
        xhr.send(data);
    }
});

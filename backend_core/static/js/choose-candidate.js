let hireBtns = document.querySelectorAll(".hire-button");

hireBtns.forEach(btn => {
    btn.onclick = function(e) {
        e.preventDefault();
        console.log("CLICK!" + btn.id);
    }
});

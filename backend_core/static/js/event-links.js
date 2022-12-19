let autoMsgs = document.querySelectorAll(".msg-text");

autoMsgs.forEach(msg => {
    if (msg.textContent.includes('AUTO MESSAGE')) {
        let words = msg.textContent.split('"');
        if (words.length === 3) {
            const eventTitle = `<a href="">` + words[1] + `</a>`;
            words[1] = eventTitle;
            msg.innerHTML = words.join(" ");
        }
    }
})

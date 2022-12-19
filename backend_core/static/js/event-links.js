let autoMsgs = document.querySelectorAll(".msg-text");

autoMsgs.forEach(msg => {
    if (msg.textContent.includes('AUTO MESSAGE')) {
        let words = msg.textContent.split('"');
        if (words.length === 3) {
            let eventTitle = words[1];
            let titleSlug = eventTitle.toLowerCase().replace(' ', '-');
            const eventTitleHtml = `<a href="/jobs/` + titleSlug + `/">` + words[1] + `</a>`;
            words[1] = eventTitleHtml;
            msg.innerHTML = words.join(" ");
            console.log(titleSlug);
        }
    }
})

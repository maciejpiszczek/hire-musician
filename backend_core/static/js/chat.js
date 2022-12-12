const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + roomName
    + '/'
);

chatSocket.onclose = function(e) {
    console.error('The socket closed unexpectedly');
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.message) {
        const now = new Date();
        let currTime = now.getHours() + ":" + now.getMinutes();

        const messageList = document.getElementById('chat-messages');
        let msg = document.createElement('div');
        let html = `<div class="row d-flex justify-content-between">
                        <div class="w-50 d-flex">
                            <h6>` + data.username + `</h6>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between">
                        <p>` + data.message + `</p>
                        <p>` + currTime + `</p>
                    </div>
                    <hr>`;
        msg.innerHTML = html;
        messageList.appendChild(msg);
        messageList.lastChild.scrollIntoView();
    } else {
        alert('The message was empty!')
    }

    scrollToBottom();
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    e.preventDefault();

    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    if (message) {
       chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName,
        'room': roomName
       }));
    }

    messageInputDom.value = '';

    return false;
};

function scrollToBottom() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}

scrollToBottom();

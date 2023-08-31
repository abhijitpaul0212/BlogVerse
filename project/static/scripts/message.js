// Timeout Alert: handles multiple Flask flash messages.
setTimeout(() => {
    let alert_message = document.getElementsByClassName("alert");

    for (let i = 0; i < alert_message.length; i++) {
        alert_message[i].style.display = "none";
    }
}, 5000);
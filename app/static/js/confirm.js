function confirmSubmission(event, action, subject) {
    const confirmation = confirm("Are you sure you want to "+ action + " this " + subject + "?");
    if (!confirmation) {
        event.preventDefault(); // Stops the form from submitting
    }
}

function confirmRedirect(event, action = "sign out", url = "/") {
    const confirmation = confirm(`Are you sure you want to ${action}?`);
    if (confirmation) {
        window.location.href = url;
    } else {
        event.preventDefault();
    }
}
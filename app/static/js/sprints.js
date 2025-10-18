let draggedTicket = null;

function dragstartHandler(event) {
    draggedTicket = event.target;
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("text/plain", event.target.id);
}

function dragoverHandler(event) {
    event.preventDefault(); // allows dropping
    event.dataTransfer.dropEffect = "move";
}

function dropHandler(event) {
    event.preventDefault();

    // Find the correct drop column
    const dropZone = event.target.closest('.column');
    if (!dropZone || !draggedTicket) return;

    // Avoid accidental duplication:
    if (!dropZone.contains(draggedTicket)) {
        dropZone.appendChild(draggedTicket);
    }

    // Optional: update backend about new status
    const newStatus = dropZone.querySelector('h2').innerText;
    const ticketId = draggedTicket.id.replace("ticket-", "");

    fetch(`/update_ticket_status/${ticketId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus })
    });
}

function showSprintInfo() {
    const selected = document.getElementById("sprintSelect").value;
    const infoDivs = document.querySelectorAll(".sprint-data");
    infoDivs.forEach(div => div.style.display = "none");

    if (selected) {
        const activeSprint = document.getElementById("sprint-" + selected);
        if (activeSprint) activeSprint.style.display = "block";
    }
}

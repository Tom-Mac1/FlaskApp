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

    // Determine new status
    const headerText = dropZone.querySelector('h2').innerText.trim();
    let newStatus = "To Do";
    if (headerText === "In Progress") newStatus = "In Progress";
    else if (headerText === "Done") newStatus = "Done";

    const ticketId = draggedTicket.id.replace("ticket-", "");
    const sprintId = currentSprintId; // use global variable

    fetch(`/update_ticket_status/${ticketId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: newStatus, sprint: sprintId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            console.log(`Ticket ${ticketId} updated to ${newStatus}`);
        } else {
            console.error("Error updating ticket:", data.error);
        }
    })
    .catch(err => console.error("Fetch error:", err));
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

function loadSprint() {
    const select = document.getElementById("sprintSelect");
    const sprintId = select.value;

    if (sprintId) {
        window.location.href = `/sprints?sprint_id=${sprintId}`;
    } else {
        window.location.href = `/sprints`;
    }
}

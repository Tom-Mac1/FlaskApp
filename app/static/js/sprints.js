function dragstartHandler(ev) {
    // Make sure we drag the .ticket-card itself
    let target = ev.target;
    while (target && !target.classList.contains("ticket-card")) {
        target = target.parentElement;
    }
    if (!target) return;

    // Store the ID for drop
    ev.dataTransfer.setData("text/plain", target.id);
    ev.dataTransfer.effectAllowed = "move";

    // Explicitly create a drag image clone to prevent ghosting
    const dragIcon = target.cloneNode(true);
    dragIcon.style.position = "absolute";
    dragIcon.style.top = "-999px";      // hide off-screen
    dragIcon.style.left = "-999px";
    document.body.appendChild(dragIcon);

    ev.dataTransfer.setDragImage(dragIcon, 10, 10);

    // Remove it after a short delay to prevent clutter
    setTimeout(() => document.body.removeChild(dragIcon), 0);
}

function dragoverHandler(ev) {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "move";
}

function dropHandler(ev) {
    ev.preventDefault();
    const data = ev.dataTransfer.getData("text/plain");
    const draggedElement = document.getElementById(data);

    // Find the nearest column
    let dropTarget = ev.target;
    while (dropTarget && !dropTarget.classList.contains("column")) {
        dropTarget = dropTarget.parentElement;
    }

    if (dropTarget && draggedElement) {
        dropTarget.appendChild(draggedElement);
    }
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

async function updateStatus() {
    setTimeout(updateStatus, 5000);
    const response = await fetch('api/status');
    if (!response.ok)
        return;
    const data = await response.json();
    for (const [key, value] of Object.entries(data)) {
        const element = document.querySelector(`[data-name="${key}"]`);
        if (!element)
            continue;
        element.dataset.status = value;
    }
}

function setDashboardItemsReaction() {
    for (const element of document.querySelectorAll('.dashboard .item')) {
        const startButton = element.querySelector('button[data-action="start"]');
        const stopButton = element.querySelector('button[data-action="stop"]');
        const indicator = element.querySelector('.indicator');
        if (!startButton || !stopButton)
            continue;
        startButton.disabled = true;
        stopButton.disabled = true;
        const observer = new MutationObserver((mutations) => {
            for (const mutation of mutations) {
                if (mutation.type !== 'attributes')
                    continue;
                const status = mutation.target.dataset.status !== 'false';
                startButton.disabled = status;
                stopButton.disabled = !status;
                indicator.querySelector('.value').innerHTML = status ? 'ON' : 'OFF';
            }
        });
        observer.observe(element, {attributes: true});

        startButton.onclick = async () => {
            await fetch(`api/items/${element.dataset.name}/start`);
        }
        stopButton.onclick = async () => {
            await fetch(`api/items/${element.dataset.name}/stop`);
        }
    }
}

window.onload = () => {
    setDashboardItemsReaction();
    updateStatus();
}

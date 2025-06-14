document.addEventListener('DOMContentLoaded', (event) => {
    fetchLayouts();
    fetchPackages();
    fetchUpgradePackages();
    fetchNetwork();
    fetchCurrentLayout();
    fetchCurrentVolume().then(() => {
        document.getElementById('volumeSlider').style.display = 'block';
    });
});

function showContent(section) {
    const contents = document.querySelectorAll('.content > div');
    contents.forEach(content => content.classList.remove('active'));
    const sectionElement = document.getElementById(section);
        sectionElement.classList.add('active');
}

function setVolume(volume) {
    fetch(`/set_volume?level=${volume}`)
        .then(response => response.json())
        .then(data => {
           document.getElementById('volumeLabel').textContent = `${volume}%`;
        })
        .catch(error => console.error('Error:', error));
}

function fetchCurrentVolume() {
    return fetch('/current_volume')
        .then(response => response.json())
        .then(data => {
            if (data.volume !== 'error') {
                document.getElementById('volumeSlider').value = data.volume;
                document.getElementById('volumeLabel').textContent = `${data.volume}%`;
            } else {
                console.error('Error fetching volume:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

function fetchPackages() {
    fetch('/get_packages')
        .then(response => response.json())
        .then(data => {
            const packages = data.packages.sort(); // Ordenar alfabeticamente
            const packageList = document.getElementById('packageList');
            packageList.innerHTML = '';
            packages.forEach(pkg => {
                const li = document.createElement('li');
                li.textContent = pkg;
                packageList.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
}

function fetchUpgradePackages() {
    fetch('/get_upgrade_packages')
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('packageList');
            resultsContainer.innerHTML = '';
            data.results.forEach(result => {
                const listItem = document.createElement('li');
                listItem.textContent = result;
                resultsContainer.appendChild(listItem);
            });
        })
        .catch(error => console.error('Erro:', error));
}

function fetchNetwork() {
    fetch('/get_network')
        .then(response => response.json())
        .then(data => {
            const networkContainer = document.getElementById('network');
            data.forEach(iface => {
                networkContainer.innerHTML += `
                    <p><strong>Interface:</strong> ${iface.interface}</p>
                    <p><strong>Tipo:</strong> ${iface.type}</p>
                    <p><strong>Fabricante:</strong> ${iface.vendor}</p>
                    <p><strong>Modelo:</strong> ${iface.product}</p>
                    <p><strong>IP LAN:</strong> ${iface.ip_lan}</p>
                    <p><strong>IP WAN:</strong> ${iface.ip_wan}</p>
                    <p><strong>Gateway:</strong> ${iface.gateway}</p>
                    <p><strong>DNS 1:</strong> ${iface.dns1}</p>
                    <p><strong>DNS 2:</strong> ${iface.dns2}</p>
                `;
                
            });
        })
        .catch(error => console.error('Erro ao buscar informações de rede:', error));
}

let previousLayout = null;
let previousLayoutElement = null;

function fetchLayouts() {
    fetch('/keyboard_layouts')
        .then(response => response.json())
        .then(data => {
            const layoutList = document.getElementById('layoutList');
            layoutList.innerHTML = '';
            data.layouts.forEach(layout => {
                const li = document.createElement('li');
                li.textContent = layout;
                li.onclick = () => openModal(layout, li);
                layoutList.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
}

function setLayout(layout, li) {
    fetch(`/set_keyboard_layout?layout=${layout}`)
        .then(response => response.json())
        .then(data => {
            document.querySelectorAll('#layoutList li').forEach(item => item.classList.remove('selected'));
            li.classList.add('selected');
        })
        .catch(error => console.error('Error:', error));
}

function fetchCurrentLayout() {
    fetch('/current_keyboard_layout')
        .then(response => response.json())
        .then(data => {
            const currentLayout = data.layout;
            const layoutListItems = document.querySelectorAll('#layoutList li');
            layoutListItems.forEach(item => {
                if (item.textContent === currentLayout) {
                    item.classList.add('selected');
                }
            });
        })
        .catch(error => console.error('Error:', error));
}

function openModal(layout, li) {
    previousLayout = document.querySelector('#layoutList li.selected')?.textContent;
    previousLayoutElement = document.querySelector('#layoutList li.selected');
    setLayout(layout, li);
    document.getElementById('testInput').value = ''; // Esvaziar o campo de texto
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    if (previousLayout && previousLayoutElement) {
        setLayout(previousLayout, previousLayoutElement);
    }
    document.getElementById('modal').style.display = 'none';
    document.getElementById('testInput').value = ''; // Esvaziar o campo de texto
}

function applyLayout() {
    previousLayout = null;
    previousLayoutElement = null;
    document.getElementById('modal').style.display = 'none';
    document.getElementById('testInput').value = ''; // Esvaziar o campo de texto
}

window.onclick = function(event) {
    if (event.target == document.getElementById('modal')) {
        closeModal();
    }
}


document.addEventListener('DOMContentLoaded', function () {
    // Ottieni i pulsanti per schermi piccoli e grandi
    const darkModeToggleSmall = document.getElementById('dark-mode-toggle-small');
    const darkModeToggleLarge = document.getElementById('dark-mode-toggle-large');

    // Funzione per attivare/disattivare la modalità scura
    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');

        // Salva la preferenza nel localStorage
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    }

    // Verifica se la modalità scura è abilitata nel localStorage al caricamento della pagina
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }

    // Aggiungi gli event listener ai pulsanti per schermi piccoli e grandi
    if (darkModeToggleSmall) {
        darkModeToggleSmall.addEventListener('click', toggleDarkMode);
    }

    if (darkModeToggleLarge) {
        darkModeToggleLarge.addEventListener('click', toggleDarkMode);
    }
});


function showLoadingSpinner() {
    // Mostra uno spinner di caricamento
    const spinnerOverlay = document.createElement('div');
    spinnerOverlay.id = 'globalLoadingOverlay';
    spinnerOverlay.innerHTML = '<div class="spinner"></div>';  // Inserisci qui il tuo spinner
    document.body.appendChild(spinnerOverlay);

    // Rimuovi lo spinner dopo 3 secondi
    setTimeout(() => {
        const spinnerOverlay = document.getElementById('globalLoadingOverlay');
        if (spinnerOverlay) {
            document.body.removeChild(spinnerOverlay);
        }
    }, 1500); // Rimuovi dopo 1 secondo (o qualsiasi valore tu desideri)
}

// Aggiungi un gestore di eventi per tutti i link nel menu
document.querySelectorAll('.load-link').forEach(link => {
    link.addEventListener('click', function(event) {
        showLoadingSpinner(); // Mostra lo spinner
    });
});


document.getElementById('logout').addEventListener('click', function() {
    fetch("/appBT/do_logout", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,  // Use the token defined in the template
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                // Check if the response contains a redirect URL
                if (data.redirect) {
                    window.location.href = data.redirect;  // Redirect to login page
                } else {
                    throw new Error(data.Error || 'Network response was not ok');
                }
            });
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        // This will only execute if the logout is successful without errors
        window.location.href = "/appBT/login";  // Redirect to login page
    })
    .catch(error => {
        console.error('Error:', error);
        // Optionally redirect to login if there's a network error
        window.location.href = "/appBT/login";  // Redirect to login page
    });
});

function disableAllSubmitButtons() {
    // Trova tutti i pulsanti di invio e quelli con la classe "action-button" o di tipo "button"
    const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"], button.action-button, input[type="button"]');
    
    submitButtons.forEach(button => {
        button.disabled = true; // Disabilita tutti i pulsanti identificati
    });
}


function goBack() {
    window.history.back();
}

// Funzione per convertire il colore esadecimale in rgba con opacità
function hexToRgba(hex, opacity) {
    hex = hex.replace('#', '');
    if (hex.length === 3) {
        hex = hex.split('').map(function (hexDigit) {
            return hexDigit + hexDigit;
        }).join('');
    }
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
}

// Applica i colori dinamici per modalità chiara e scura
document.querySelectorAll('.card').forEach(item => {
    const backgroundColor = item.getAttribute('data-color'); // Colore dinamico
    const fadedColor = hexToRgba(backgroundColor, 0.2); // Sbiadito al 20% di opacità

    // Determina il colore di sfondo di default dalla modalità corrente
    const defaultBgColor = getComputedStyle(document.documentElement)
        .getPropertyValue('--card-bg-light')
        .trim();

    item.addEventListener('mouseenter', function () {
        item.style.backgroundColor = fadedColor; // Sfondo sbiadito
    });

    item.addEventListener('mouseleave', function () {
        item.style.backgroundColor = defaultBgColor; // Ritorna al colore base
    });
});
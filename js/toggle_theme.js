function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName + " colors";
}

function checkTheme() {
    if (localStorage.getItem('theme') === 'theme-dark') {
        setTheme('theme-dark');
    } else {
        setTheme('theme-light');
    }
}

checkTheme();

let toggleThemeButton = document.getElementById("btn-toggle-theme");

if (toggleThemeButton !== null) {
    toggleThemeButton.addEventListener('click', function () {
        toggleTheme();
    });
}

function toggleTheme() {
    if (localStorage.getItem('theme') === 'theme-dark'){
        setTheme('theme-light');
    } else {
        setTheme('theme-dark');
    }
}


function setCurrentMenu(menuName) {
    localStorage.setItem('menu', menuName);
}

let currentSettingMenu = document.getElementById("current-settings-menu");
let generalOption = document.getElementById("general");
let appearanceOption = document.getElementById("appearance");
let topicsOption = document.getElementById("topics");
generalOption.addEventListener("click", general);
appearanceOption.addEventListener("click", appearance);
topicsOption.addEventListener("click", topics);

function general() {
    setCurrentMenu("general-option");
    currentSettingMenu.innerHTML = document.getElementById("general-option").innerHTML;
}

function appearance() {
    setCurrentMenu("appearance-option");
    currentSettingMenu.innerHTML = document.getElementById("appearance-option").innerHTML;
}

function topics() {
    setCurrentMenu("topics-option");
    currentSettingMenu.innerHTML = document.getElementById("topics-option").innerHTML;
}

function empty() {
    currentSettingMenu.innerHTML = "";
}

(function () {
    switch (localStorage.getItem('menu')) {
        case 'general-option':
            general();
            break;
        case 'appearance-option':
            appearance();
            break;
        case 'topics-option':
            topics();
            break;
        default:
            empty();
    }

})();

window.unload = () => {
    window.localStorage.removeItem('menu');
}
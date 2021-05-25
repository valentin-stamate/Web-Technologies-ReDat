import {refreshTopics} from "./topics.js";
import {initListeners} from "./user_profile.js";

function setCurrentMenu(menuName) {
    localStorage.setItem('menu', menuName);
}

let currentSettingMenu = document.getElementById("current-settings-menu");

let generalOption = document.getElementById("general");
let appearanceOption = document.getElementById("appearance");
let topicsOption = document.getElementById("topics");

const generalOptionsElement = document.getElementById("general-option");
const generalOptionsHTML = generalOptionsElement.innerHTML;
generalOptionsElement.innerHTML = '';

const appearanceOptionsElement = document.getElementById("appearance-option");
const appearanceOptionsHTML = appearanceOptionsElement.innerHTML;
appearanceOptionsElement.innerHTML = '';

const topicOptionsElement = document.getElementById("topics-option");
const topicOptionsHTML = topicOptionsElement.innerHTML;
topicOptionsElement.innerHTML = '';

generalOption.addEventListener("click", general);
appearanceOption.addEventListener("click", appearance);
topicsOption.addEventListener("click", topics);

function general() {
    setCurrentMenu("general-option");
    currentSettingMenu.innerHTML = generalOptionsHTML;
    initListeners()
}

function appearance() {
    setCurrentMenu("appearance-option");
    currentSettingMenu.innerHTML = appearanceOptionsHTML;

    toggleThemeButton = document.getElementById("btn-toggle-theme");
    toggleThemeButton.addEventListener('click', function () {
        toggleTheme();
    });
}

function topics() {
    setCurrentMenu("topics-option");
    currentSettingMenu.innerHTML = topicOptionsHTML;
    refreshTopics();
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

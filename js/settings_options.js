let currentSettingMenu = document.getElementById("profile-component");
let generalOption = document.getElementById("general");
let appearanceOption = document.getElementById("appearance");
let topicsOption = document.getElementById("topics");
generalOption.addEventListener("click", general);
appearanceOption.addEventListener("click", appearance);
topicsOption.addEventListener("click", topics);

function general(blob, encoding) {
    const divContent = "general content";
    currentSettingMenu.innerHTML = divContent;
}

function appearance() {
    const divContent = "Appearance content";
    currentSettingMenu.innerHTML = divContent;
}

function topics() {
    const divContent = "topics content";
    currentSettingMenu.innerHTML = divContent;
}
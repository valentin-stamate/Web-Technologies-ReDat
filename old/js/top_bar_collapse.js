let coll = document.getElementById("top-bar-collapse-icon");

coll.addEventListener("click", function() {
    this.classList.toggle("active");
    let content = document.getElementById("top-bar-collapse-content");

    if (content.style.maxHeight) {
        content.style.maxHeight = null;
    } else {
        content.style.maxHeight = content.scrollHeight + "px";
    }
});


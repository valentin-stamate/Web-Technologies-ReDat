function getFormData(form) {
    return Object.fromEntries(new FormData(form));
}

function parseHTML(html) {
    const t = document.createElement('template');
    t.innerHTML = html;
    return t.content;
}

export {getFormData, parseHTML}
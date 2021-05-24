function getFormData(form) {
    return Object.fromEntries(new FormData(form));
}

function parseHTML(html) {
    const t = document.createElement('template');
    t.innerHTML = html;
    return t.content;
}

function openLink(link, target='_blank') {
    window.open(link, target);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export {getFormData, parseHTML, openLink, sleep}
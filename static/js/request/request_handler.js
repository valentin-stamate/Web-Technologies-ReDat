export function sendRequest(URL, METHOD, payload) {
    const request = new XMLHttpRequest();

    request.open(METHOD, URL);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    request.send(JSON.stringify(payload));
    return request;
}

export async function sendFetchRequest(url, method, payload) {
    return await fetch(url, {
        method: method,
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(payload)
    });
}
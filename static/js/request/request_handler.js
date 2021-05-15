export function sendRequest(URL, METHOD, payload) {
    const request = new XMLHttpRequest();

    request.open(METHOD, URL);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    request.send(JSON.stringify(payload));
    console.log(JSON.stringify(payload))
    return request;
}
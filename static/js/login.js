import {getFormData} from "./util/util.js";
import {LOGIN_ENDPOINT} from "./endpoints.js";
import {sendRequest} from "./request/request_handler.js";

const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', onLogin)

function onLogin(e) {
    e.preventDefault();

    const currentTarget = e.currentTarget;

    const payload = getFormData(currentTarget);

    const request = sendRequest(LOGIN_ENDPOINT, "POST", payload);
    request.onreadystatechange = (e) => {
        if (request.readyState === XMLHttpRequest.DONE) {
            console.log(JSON.parse(request.responseText));
        }
    }
}
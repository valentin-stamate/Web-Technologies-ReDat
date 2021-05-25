import {getFormData} from "./util/util.js";
import {LOGIN_ENDPOINT} from "./endpoints.js";
import {sendRequest} from "./request/request_handler.js";
import {setCookie, deleteCookies, USER_AUTH_COOKIE} from "./util/cookie.js";

deleteCookies()

const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', onLogin)

function onLogin(e) {
    e.preventDefault();

    const currentTarget = e.currentTarget;

    const payload = getFormData(currentTarget);

    const request = sendRequest(LOGIN_ENDPOINT, "POST", payload);
    request.onreadystatechange = (e) => {
        if (request.readyState === XMLHttpRequest.DONE) {
            const status = request.status;
            const errorTextElement = document.getElementById('error-text');
            errorTextElement.innerHTML = '';

            if (status === 200) {
                setCookie(USER_AUTH_COOKIE, JSON.parse(request.responseText).token);
                window.location = "/home"
            } else {
                errorTextElement.innerHTML = request.responseText;
            }
        }
    }
}
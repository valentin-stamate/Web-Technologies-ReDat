import {getFormData} from "./util/util.js";
import {sendRequest} from "./request/request_handler.js";
import {REGISTER_ENDPOINT} from "./endpoints.js";
import {setCookie, USER_AUTH_COOKIE} from "./util/cookie.js";

const registerForm = document.getElementById('register-form');

registerForm.addEventListener('submit', onRegister)

function onRegister(e) {
    e.preventDefault();

    const currentTarget = e.currentTarget;

    const payload = getFormData(currentTarget);

    console.log(getFormData(currentTarget));

    const request = sendRequest(REGISTER_ENDPOINT, "POST", payload);
    request.onreadystatechange = (e) => {
        if (request.readyState === XMLHttpRequest.DONE) {
            const status = request.status;

            // if (status === 200) {
            //     setCookie(USER_AUTH_COOKIE, JSON.parse(request.responseText).userAuth);
            // }
            /* TODO else, display the errors */
        }
    }
}
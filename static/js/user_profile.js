import {getFormData} from "./util/util.js";
import {UPDATE_USER_ENDPOINT} from "./endpoints.js";
import {sendFetchRequest} from "./request/request_handler.js";
import {getCookie, USER_AUTH_COOKIE} from "./util/cookie.js";

export function initListeners() {
    const userDataForm = document.getElementById('user-data-form');
    const saveButton = document.getElementById('save-button');

    saveButton.addEventListener('click', function(e) {
        e.preventDefault();
        const userData = getFormData(userDataForm);

        sendFetchRequest(UPDATE_USER_ENDPOINT, 'POST', {'token': getCookie(USER_AUTH_COOKIE), ...userData})
            .then(response => {
                const errorTextElement = document.getElementById('error-text-user-data');
                errorTextElement.innerHTML = '';

                if (response.status === 200) {
                    console.log("Success")
                    window.location = '/profile';
                } else {
                    response.json().then(data => {
                        errorTextElement.innerHTML = data.message;
                    })
                }
            });
    });
}

initListeners();


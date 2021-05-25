import {getFormData} from "./util/util.js";
import {UPDATE_USER_ENDPOINT} from "./endpoints.js";
import {sendFetchRequest} from "./request/request_handler.js";
import {getCookie, USER_AUTH_COOKIE} from "./util/cookie.js";

const userDataForm = document.getElementById('user-data-form');
const saveButton = document.getElementById('save-button');
saveButton.addEventListener('click', function(e) {
    e.preventDefault();
    const userData = getFormData(userDataForm);

    sendFetchRequest(UPDATE_USER_ENDPOINT, 'POST', {'token': getCookie(USER_AUTH_COOKIE), ...userData})
        .then(response => {
            return response.text();
        })
        .then(data => {
            window.location = '/profile';
        });
    /* TODO error checking */

});

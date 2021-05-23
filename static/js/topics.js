import {sendFetchRequest} from "./request/request_handler.js";
import {DELETE_TOPIC_ENDPOINT} from "./endpoints.js";
import {getCookie, USER_AUTH_COOKIE} from "./util/cookie.js";


function onDeleteTopic(e) {
    e.preventDefault();

    const target = e.target;
    const parent = target.parentElement

    const topicId = target.getAttribute('data-id');

    sendFetchRequest(DELETE_TOPIC_ENDPOINT, 'DELETE', {'token': getCookie(USER_AUTH_COOKIE), 'topic_id': topicId})
        .then(response => {
            if (response.status === 200) {
                /* TODO, do something */
            } else {
                /* TODO failure */
            }
            return response.json();
        });

    parent.remove();
}

const buttons = document.getElementsByClassName('chip-delete-button');

for (let i = 0; i < buttons.length; i++) {
    const button = buttons[i];
    button.addEventListener('click', onDeleteTopic);
}
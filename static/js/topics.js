import {sendFetchRequest} from "./request/request_handler.js";
import {ADD_TOPIC_ENDPOINT, ALL_TOPICS_ENDPOINT, DELETE_TOPIC_ENDPOINT, USER_TOPICS_ENDPOINT} from "./endpoints.js";
import {getCookie, USER_AUTH_COOKIE} from "./util/cookie.js";
import {parseHTML} from "./util/util.js";

let allRawTopics = []
let userRawTopics = []

function fetchUserTopics() {
    sendFetchRequest(USER_TOPICS_ENDPOINT, 'POST', {'token': getCookie(USER_AUTH_COOKIE)})
        .then(response => response.json())
        .then(data => {
            userRawTopics = []
            userRawTopics.push(...data);

            const userTopicsContainer = document.getElementsByClassName("user-preferences")[0];
            userTopicsContainer.innerHTML = '';

            for (let i = 0; i < userRawTopics.length; i++) {
                const rawItem = userRawTopics[i];
                const item = parseHTML(`<div class='button-chip'><button data-id='${rawItem.topic_id}' class='chip-delete-button'>x</button><b>${rawItem.name}</b></div>`)
                userTopicsContainer.append(item);
            }

            listenOnDeleteTopic();
        });
}

function fetchAllTopics() {
    sendFetchRequest(ALL_TOPICS_ENDPOINT, 'POST', {'token': getCookie(USER_AUTH_COOKIE)})
        .then(response => response.json())
        .then(data => {
            allRawTopics = []
            allRawTopics.push(...data);

            const allTopicsContainer = document.getElementsByClassName("all-topics-container")[0];
            allTopicsContainer.innerHTML = '';

            for (let i = 0; i < allRawTopics.length; i++) {
                const rawItem = allRawTopics[i];

                let found = false;
                for (let j = 0; j < userRawTopics.length && !found; j++) {
                    if (rawItem.topic_id === userRawTopics[j].topic_id) {
                        found = true;
                    }
                }

                if (found) {
                    continue;
                }

                const item = parseHTML(`<div class="topic-list-item">
                                                <div><b>${rawItem.name}</b></div>
                                                <button data-id="${rawItem.topic_id}" class="button primary add-topic-button">Add</button>
                                             </div>`)

                allTopicsContainer.append(item);
            }

            listenOnAddTopic();
        });
}

function listenOnDeleteTopic() {
    const buttons = document.getElementsByClassName("chip-delete-button");

    for (let i = 0; i < buttons.length; i++) {
        const button = buttons[i];
        button.addEventListener('click', onDeleteTopic);
    }
}

function listenOnAddTopic() {
    const buttons = document.getElementsByClassName('add-topic-button');

    for (let i = 0; i < buttons.length; i++) {
        const button = buttons[i];
        button.addEventListener('click', onAddTopic);
    }
}

function onDeleteTopic(e) {
    e.preventDefault();

    const target = e.target;
    const topicId = target.getAttribute('data-id');

    sendFetchRequest(DELETE_TOPIC_ENDPOINT, 'DELETE', {'token': getCookie(USER_AUTH_COOKIE), 'topic_id': topicId})
        .then(response => {
            if (response.status === 200) {
                refreshTopics();
            } else {
                /* TODO failure */
            }
            return response.json();
        });
}

function onAddTopic(e) {
    e.preventDefault();

    const target = e.target;
    const topicId = target.getAttribute('data-id');

    sendFetchRequest(ADD_TOPIC_ENDPOINT, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'topic_id': topicId})
        .then(response => {
            if (response.status === 200) {
                refreshTopics();
            } else {
                /* TODO error */
            }
            return response.json();
        });
}

refreshTopics();

function refreshTopics() {
    fetchUserTopics();
    fetchAllTopics();
}

const startButton = document.getElementById('start-exploring-button');
startButton.addEventListener('click', function (e) {
    document.location = '/home';
});
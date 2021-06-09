import {sendFetchRequest} from "./request/request_handler.js";
import {ADMIN_ADD_ADMIN, ADMIN_ADD_TOPIC, ADMIN_REMOVE_TOPIC, ALL_TOPICS_ENDPOINT} from "./endpoints.js";
import {getCookie, USER_AUTH_COOKIE} from "./util/cookie.js";
import {parseHTML} from "./util/util.js";

const topicInput = document.getElementById('add-topic-input');
const topicButton = document.getElementById('topic-button');
const topicsWrapper = document.getElementsByClassName('admin-user-list')[0];

topicButton.addEventListener('click',  async () => {
    const topicName = topicInput.value;
    await addTopic(topicName);
})

async function fetchAllTopics() {
    let allRawTopics = [];

    await sendFetchRequest(ALL_TOPICS_ENDPOINT, 'POST', {'token': getCookie(USER_AUTH_COOKIE)})
        .then(response => response.json())
        .then(data => {allRawTopics.push(...data);});

    return allRawTopics;
}

async function refreshTopics() {
    const allTopics = await fetchAllTopics();
    topicsWrapper.innerHTML = '';

    for (let i = 0; i < allTopics.length; i++) {
        const topic = allTopics[i];
        const topicItemTemplate = `
                <div class="user-item">
                    <div>${topic.name}</div>
                    <div class="flex-right"></div>
                    <a href="${topic.url}" target="_blank"><button class="button primary">Link</button></a>
                    <div><button class="button primary" id="remove-topic-button-${i}">Remove</button></div>
                </div>`

        topicsWrapper.append(parseHTML(topicItemTemplate));

        const removeButton = document.getElementById(`remove-topic-button-${i}`);
        removeButton.addEventListener('click', () => {removeTopic(topic.name)});
    }
}

refreshTopics().then();

async function removeTopic(topicName) {
    await sendFetchRequest(ADMIN_REMOVE_TOPIC, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'topic_name': topicName})

    await refreshTopics();
}

async function addTopic(topicName) {
    await sendFetchRequest(ADMIN_ADD_TOPIC, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'topic_name': topicName})

    await refreshTopics();
}

import {parseHTML, sleep} from "./util/util.js";
import {sendFetchRequest} from "./request/request_handler.js";
import {
    CHECK_COMMENTS_ENDPOINT,
    STATISTIC_COMMENTS_ENDPOINT, STATISTIC_DOWNS,
    STATISTIC_GENERAL_ENDPOINT, STATISTIC_UPS_DOWNS_ENDPOINT,
    UPVOTE_RATIO_ENDPOINT,
    USER_TOPICS_ENDPOINT
} from "./endpoints.js";
import {getCookie, USER_AUTH_COOKIE} from "./util/cookie.js";

let firstFetching = true;

let userRawTopics = [];
const comments = new Map();
const notificationActivated = new Map();

async function fetchUserTopics() {
    await sendFetchRequest(USER_TOPICS_ENDPOINT, 'POST', {'token': getCookie(USER_AUTH_COOKIE)})
        .then(response => response.json())
        .then(data => {
            userRawTopics = [];
            userRawTopics.push(...data);
        });
    await fetchPosts(userRawTopics);
}



async function fetchPosts(topics) {
    const generalStatisticWrapper = document.getElementsByClassName('subreddits-container-statistics')[0];

    const generalStatisticSVG = await getGeneralStatistic();
    const generalStatisticTemplate = `<div></div>
                                      <div>
                                          <img style="width: 800px; height: auto;" class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${generalStatisticSVG}" alt="">
                                          <div class="statistics-item-buttons">
                                              <button class="button primary" id="statistic-upvote" onclick="downloadSVG('general.svg', '${generalStatisticSVG}')">SVG</button>
                                          </div>
                                      </div>
                                      <div></div>`;

    generalStatisticWrapper.innerHTML = generalStatisticTemplate;

    const postsWrapper = document.getElementsByClassName('subreddits-wrapper-list')[1];
    let topicListElement = [];

    for (let i = 0; i < topics.length; i++) {
        const topic = topics[i];

        if (comments.get(topic.name) === undefined) {
            comments.set(topic.name, 0);
            notificationActivated.set(topic.name, false);
        }

        const currentComments = comments.get(topic.name);
        const commentsObj = await getComments(topic.name, currentComments);

        const newComments = commentsObj.comments_number;

        comments.set(topic.name, newComments);

        if (currentComments !== newComments && currentComments !== 0) {
            notificationActivated.set(topic.name, true);
        }

        const notificationActive = notificationActivated.get(topic.name);
        const notificationHtml = notificationActive ?
            `<span class="material-icons flex-right topic-notification" data-id="${topic.name}">notifications_active</span>` :
            `<span class="material-icons flex-right topic-notification" data-id="${topic.name}">notifications</span>`;

        let arrayStatistics = ``;

        const upVoteRationSVG = await getUpVoteRationSVG(topic.name);
        const upVoteTemplate = `<div>
                                    <img class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${upVoteRationSVG}" alt="">
                                    <div class="statistics-item-buttons">
                                        <button class="button primary" id="statistic-upvote" onclick="downloadSVG('${topic.name}_upvote_ratio.svg', '${upVoteRationSVG}')">SVG</button>
                                        <button class="button primary" id="statistic-upvote" onclick="downloadCSVUpVoteRatio('${topic.name}')">CSV</button>
                                    </div>
                                </div>`;

        const commentsSVG = await getCommentsStatistic(topic.name);
        const commentsTemplate = `<div>
                                      <img class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${commentsSVG}" alt="">
                                      <div class="statistics-item-buttons">
                                        <button class="button primary" id="statistic-upvote" onclick="downloadSVG('${topic.name}_comments.svg', '${commentsSVG}')">SVG</button>
                                        <button class="button primary" id="statistic-upvote" onclick="downloadCSVComments('${topic.name}')">CSV</button>
                                      </div>
                                  </div>`;

        const upDownSVG = await getUpsDownsStatistics(topic.name);
        const upDownTemplate = `<div>
                                    <img class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${upDownSVG}" alt="">
                                    <div class="statistics-item-buttons">
                                        <button class="button primary" id="statistic-upvote" onclick="downloadSVG('${topic.name}_ups_downs.svg', '${upDownSVG}')">SVG</button>
                                        <button class="button primary" id="statistic-upvote" onclick="downloadCSVUpsDowns('${topic.name}')">CSV</button>
                                    </div>
                                </div>`;

        arrayStatistics += upVoteTemplate;
        arrayStatistics += commentsTemplate;
        arrayStatistics += upDownTemplate;

        const postHTML = `<div class="subreddits-container">
                                <div class="subreddits-container-top">
                                    <div class="subreddits-container-name"><b>/r/${topic.name}</b></div>
                                
                                    <div class="subreddits-container-notification">
                                        ${notificationHtml}
                                        <div>Comments: ${comments.get(topic.name)}</div>
                                    </div>
                                </div>
                                
                                <div class="subreddits-container-statistics">
                                    ${arrayStatistics}
                                </div>
                                
                                <div class="subreddits-container-bottom" data-id="${topic.topic_id}">
                                    <a class="button primary open-topic-button" href="${topic.url}" target="_blank" data-id="${topic.name}">Open</a>
                                    <div class="flex-right"/>
                                </div>
                            </div>`

        const itemElement = parseHTML(postHTML);
        if (firstFetching) {
            postsWrapper.append(itemElement);
            continue;
        }

        topicListElement.push(itemElement);
    }

    if (!firstFetching) {
        postsWrapper.innerHTML = '';
        for (let i = 0; i < topicListElement.length; i++) {
            postsWrapper.append(topicListElement[i]);
        }
    }

    firstFetching = false;

    await initializeOpenTopicButtonListener();
}

async function initializeOpenTopicButtonListener() {
    const openButtons = document.getElementsByClassName("open-topic-button");

    for (let i = 0; i < openButtons.length; i++) {
        const openButton = openButtons[i];
        const topicName = openButton.getAttribute('data-id');

        /* DEACTIVATE NOTIFICATION */
        openButton.addEventListener('click', function () {
            const notification = document.querySelector(`.topic-notification[data-id='${topicName}']`);

            notification.innerHTML = 'notifications';
            notificationActivated.set(topicName, false);
        });
    }
}

async function getGeneralStatistic() {
    let statisticSVG = '';
    await sendFetchRequest(STATISTIC_GENERAL_ENDPOINT, 'POST', {})
        .then(result => result.text())
        .then(data => statisticSVG = data);

    return window.btoa(statisticSVG);
}

async function getUpVoteRationSVG(topicName) {
    let statisticSVG = '';
    await sendFetchRequest(UPVOTE_RATIO_ENDPOINT, 'POST', {'topic': topicName})
            .then(result => result.text())
            .then(data => statisticSVG = data);

    return window.btoa(statisticSVG);
}

async function getCommentsStatistic(topicName) {
    let statisticSVG = '';
    await sendFetchRequest(STATISTIC_COMMENTS_ENDPOINT, 'POST', {'topic': topicName})
        .then(result => result.text())
        .then(data => statisticSVG = data);

    return window.btoa(statisticSVG);
}

async function getUpsDownsStatistics(topicName) {
    let statisticSVG = '';
    await sendFetchRequest(STATISTIC_UPS_DOWNS_ENDPOINT, 'POST', {'topic': topicName})
        .then(result => result.text())
        .then(data => statisticSVG = data);

    return window.btoa(statisticSVG);
}

async function getComments(topicName, currentComments = 0) {
    let body = '';
    await sendFetchRequest(CHECK_COMMENTS_ENDPOINT, 'POST', {'topic': topicName, 'comments_number': currentComments})
        .then(result => result.json())
        .then(data => body = data);

    return body;
}

async function startFetching() {

    while (true) {
        await fetchUserTopics();
        await sleep(2000);
    }
}

startFetching();
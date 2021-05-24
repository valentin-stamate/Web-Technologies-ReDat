import {parseHTML} from "./util/util.js";
import {sendFetchRequest} from "./request/request_handler.js";
import {
    STATISTIC_COMMENTS_ENDPOINT, STATISTIC_DOWNS,
    STATISTIC_GENERAL_ENDPOINT, STATISTIC_UPS_DOWNS_ENDPOINT,
    UPVOTE_RATIO_ENDPOINT,
    USER_TOPICS_ENDPOINT
} from "./endpoints.js";
import {getCookie, USER_AUTH_COOKIE} from "./util/cookie.js";

let userRawTopics = [];

function fetchUserTopics() {
    sendFetchRequest(USER_TOPICS_ENDPOINT, 'POST', {'token': getCookie(USER_AUTH_COOKIE)})
        .then(response => response.json())
        .then(data => {
            userRawTopics = [];
            userRawTopics.push(...data);

            fetchPosts(userRawTopics);
        });
}

async function fetchPosts(topics) {
    const generalStatisticWrapper = document.getElementsByClassName('subreddits-container-statistics')[0];

    const generalStatisticSVG = await getGeneralStatistic();
    const generalStatisticTemplate = `<div></div><img style="width: 800px; height: auto;" class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${generalStatisticSVG}" alt=""><div></div>`;

    generalStatisticWrapper.innerHTML = generalStatisticTemplate;

    const postsWrapper = document.getElementsByClassName('subreddits-wrapper-list')[1];
    postsWrapper.innerHTML = '';

    for (let i = 0; i < topics.length; i++) {
        const topic = topics[i];

        const notificationActive = true;
        const notificationHtml = notificationActive ?
            `<span class="material-icons flex-right">notifications_active</span>` :
            `<span class="material-icons flex-right">notifications</span>`;

        let arrayStatistics = ``;

        const upVoteRationSVG = await getUpVoteRationSVG(topic.name);
        const upVoteTemplate = `<img class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${upVoteRationSVG}" alt="">`;

        // const downVoteSVG = await getDownVoteStatistics(topic.name);
        // const downVoteTemplate = `<img class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${downVoteSVG}" alt="">`;

        const commentsSVG = await getCommentsStatistic(topic.name);
        const commentsTemplate = `<img class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${commentsSVG}" alt="">`;

        const upDownSVG = await getUpsDownsStatistics(topic.name);
        const upDownTemplate = `<img class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${upDownSVG}" alt="">`;

        arrayStatistics += upVoteTemplate;
        // arrayStatistics += downVoteTemplate;
        arrayStatistics += commentsTemplate;
        arrayStatistics += upDownTemplate;

        const postHTML = `<div class="subreddits-container">
                                <div class="subreddits-container-top">
                                    <div class="subreddits-container-name"><b>${topic.name}</b></div>
                                
                                    <div class="subreddits-container-notification">
                                        ${notificationHtml}
                                        <div>Comments: 432</div>
                                    </div>
                                </div>
                                
                                <div class="subreddits-container-statistics">
                                    ${arrayStatistics}
                                </div>
                                
                                <div class="subreddits-container-bottom">
                                    <button class="chip">Topic A</button>
                                </div>
                            </div>`

        const postElement = parseHTML(postHTML);

        postsWrapper.append(postElement);

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

// async function getDownVoteStatistics(topicName) {
//     let statisticSVG = '';
//     await sendFetchRequest(STATISTIC_DOWNS, 'POST', {'topic': topicName})
//         .then(result => result.text())
//         .then(data => statisticSVG = data);
//
//     return window.btoa(statisticSVG);
// }

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


fetchUserTopics();
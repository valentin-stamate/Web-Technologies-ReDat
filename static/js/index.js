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
    postsWrapper.innerHTML = '';

    for (let i = 0; i < topics.length; i++) {
        const topic = topics[i];

        const notificationActive = true;
        const notificationHtml = notificationActive ?
            `<span class="material-icons flex-right">notifications_active</span>` :
            `<span class="material-icons flex-right">notifications</span>`;

        let arrayStatistics = ``;

        const upVoteRationSVG = await getUpVoteRationSVG(topic.name);
        const upVoteTemplate = `<div>
                                    <img class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${upVoteRationSVG}" alt="">
                                    <div class="statistics-item-buttons">
                                        <button class="button primary" id="statistic-upvote" onclick="downloadSVG('${topic.name}_upvote_ratio.svg', '${upVoteRationSVG}')">SVG</button>
                                        <button class="button primary" id="statistic-upvote" onclick="downloadCSVUpVoteRatio('${topic.name}')">CSV</button>
                                    </div>
                                </div>`;

        // const downVoteSVG = await getDownVoteStatistics(topic.name);
        // const downVoteTemplate = `<img class="subreddits-container-statistics-item" src="data:image/svg+xml;base64,${downVoteSVG}" alt="">`;

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
                                
                                <div class="subreddits-container-bottom" data-id="${topic.topic_id}">
                                    <a class="button primary" href="${topic.url}" target="_blank">Open</a>
                                    <div class="flex-right"/>
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
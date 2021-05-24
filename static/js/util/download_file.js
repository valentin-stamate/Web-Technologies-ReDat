const DEPLOY = ""

const STATISTIC_UPVOTE_ENDPOINT = DEPLOY + "/statistic/csv/upvote_ratio";
const STATISTIC_COMMENTS_ENDPOINT = DEPLOY + "/statistic/csv/comments";
const STATISTIC_UPS_ENDPOINT = DEPLOY + "/statistic/csv/ups";
const STATISTIC_DOWNS_ENDPOINT = DEPLOY + "/statistic/csv/downs";

async function downloadCSVUpVoteRatio(topicName) {
    const content = await getFile(STATISTIC_UPVOTE_ENDPOINT, {'topic': topicName});
    const fileName = topicName + '_upvote_ratio.csv';
    downloadFile(fileName, content, fileName);
}

async function downloadCSVComments(topicName) {
    const content = await getFile(STATISTIC_COMMENTS_ENDPOINT, {'topic': topicName});
    const fileName = topicName + '_comments.csv';
    downloadFile(fileName, content, fileName);
}

async function downloadCSVUpsDowns(topicName) {
    const contentUps = await getFile(STATISTIC_UPS_ENDPOINT, {'topic': topicName});
    const fileNameUps = topicName + '_ups.csv';
    downloadFile(fileNameUps, contentUps, fileNameUps);

    const contentDowns = await getFile(STATISTIC_DOWNS_ENDPOINT, {'topic': topicName});
    const fileNameDowns = topicName + '_downs.csv';
    downloadFile(fileNameDowns, contentDowns, fileNameDowns);
}

async function getFile(url, payload, method = 'POST') {
    let content = '';
    await sendFetchRequest(url, method, payload)
        .then(result => result.text())
        .then(data => content = data);
    return content;
}

async function sendFetchRequest(url, method, payload) {
    return await fetch(url, {
        method: method,
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(payload)
    });
}

function downloadSVG(fileName, content) {
    content = window.atob(content);
    downloadFile(fileName + '.svg', content, fileName + '.svg');
}

function downloadFile(filename, input, output, data='data:text/plain;charset=utf-8') {
    const element = document.createElement('a');
    element.setAttribute('href', data + ',' + encodeURIComponent(input));
    element.setAttribute('download', filename);
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}


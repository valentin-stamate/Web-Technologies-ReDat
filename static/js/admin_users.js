import {sendFetchRequest} from "./request/request_handler.js";
import {
    ADMIN_ADD_ADMIN,
    ADMIN_REMOVE_ADMIN,
    ADMIN_REMOVE_USER,
    ADMIN_SEARCH_USER,
    UPDATE_USER_ENDPOINT
} from "./endpoints.js";
import {getCookie, USER_AUTH_COOKIE} from "./util/cookie.js";
import {parseHTML} from "./util/util.js";

const searchUserButton = document.getElementById('search-user-button');
const searchUserInput = document.getElementById('input-search-user');
const errorTextElement = document.getElementsByClassName('error-text')[0];
const usersContainer = document.getElementsByClassName('admin-user-list')[0];

searchUserButton.addEventListener('click', async function () {
    const username = searchUserInput.value;

    await searchUser(username);
});

async function searchUser(text) {
    const request = await sendFetchRequest(ADMIN_SEARCH_USER, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'pattern': text});

    let payload = {};
    await request.json().then(data => payload = data);

    usersContainer.innerHTML = '';
    errorTextElement.innerHTML = '';

    if (request.status !== 200) {
        errorTextElement.innerHTML = payload.message;
    } else {

        for (let i = 0; i < payload.length; i++) {
            const userData = payload[i];

            const userListItem = `
                    <div class="user-item">
                        <div>${userData.username}</div>
                        <div class="flex-right"></div>
                        <div><button id="make-admin-button-${i}" class="button primary">${userData.is_admin ? "Remove Admin" : "Make Admin"}</button></div>
                        <div><button id="remove-button-${i}" class="button primary">Remove</button></div>
                    </div>`;

            const userItem = parseHTML(userListItem);

            usersContainer.append(userItem);

            const adminButton = document.getElementById('make-admin-button-' + i);
            const removeButton = document.getElementById('remove-button-' + i);

            adminButton.addEventListener('click', () => {makeAdmin(userData.username, userData.is_admin)});
            removeButton.addEventListener('click', () => {removeUser(userData.username)});
        }

    }
}

async function makeAdmin(username, isAdmin) {
    if (isAdmin === false) {
        await sendFetchRequest(ADMIN_ADD_ADMIN, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'username': username});
    } else {
        await sendFetchRequest(ADMIN_REMOVE_ADMIN, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'username': username});
    }

    const pattern = searchUserInput.value;
    await searchUser(pattern);
}

async function removeUser(username) {
    await sendFetchRequest(ADMIN_REMOVE_USER, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'username': username});

    const pattern = searchUserInput.value;
    await searchUser(pattern);
}

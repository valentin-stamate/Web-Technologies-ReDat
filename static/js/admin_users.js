import {sendFetchRequest} from "./request/request_handler.js";
import {
    ADMIN_ADD_ADMIN,
    ADMIN_REMOVE_ADMIN,
    ADMIN_REMOVE_USER,
    ADMIN_SEARCH_USER,
    UPDATE_USER_ENDPOINT
} from "./endpoints.js";
import {getCookie, USER_AUTH_COOKIE} from "./util/cookie.js";

const searchUserButton = document.getElementById('search-user-button');
const searchUserInput = document.getElementById('input-search-user');
const errorTextElement = document.getElementsByClassName('error-text')[0];
const usersContainer = document.getElementsByClassName('admin-user-list')[0];

searchUserButton.addEventListener('click', async function () {
    const username = searchUserInput.value;

    await searchUser(username);
});

async function searchUser(text) {
    const request = await sendFetchRequest(ADMIN_SEARCH_USER, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'username': text});

    let payload = {};
    await request.json().then(data => payload = data);

    if (request.status !== 200) {
        errorTextElement.innerHTML = payload.message;
    } else {
        const userListItem = `
                <div class="user-item">
                    <div>${payload.username}</div>
                    <div class="flex-right"></div>
                    <div><button id="make-admin-button" class="button primary">${payload.is_admin ? "Remove Admin" : "Make Admin"}</button></div>
                    <div><button id="remove-button" class="button primary">Remove</button></div>
                </div>`;

        usersContainer.innerHTML = userListItem;

        const adminButton = document.getElementById('make-admin-button');
        const removeButton = document.getElementById('remove-button');

        adminButton.addEventListener('click', () => {makeAdmin(payload.username, payload.is_admin)});
        removeButton.addEventListener('click', () => {removeUser(payload.username)});
    }
}

async function makeAdmin(username, isAdmin) {
    if (isAdmin === false) {
        await sendFetchRequest(ADMIN_ADD_ADMIN, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'username': username});
    } else {
        await sendFetchRequest(ADMIN_REMOVE_ADMIN, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'username': username});
    }

    await searchUser(username);
}

async function removeUser(username) {
    await sendFetchRequest(ADMIN_REMOVE_USER, 'POST', {'token': getCookie(USER_AUTH_COOKIE), 'username': username});

    usersContainer.innerHTML = "";
}

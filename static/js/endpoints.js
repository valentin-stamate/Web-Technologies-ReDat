const DEPLOY = ""

export const LOGIN_ENDPOINT = DEPLOY + "/auth_user";
export const REGISTER_ENDPOINT = DEPLOY + "/register_user";
export const ADD_TOPIC_ENDPOINT = DEPLOY + "/user_add_topic";
export const DELETE_TOPIC_ENDPOINT = DEPLOY + "/user_delete_topic";
export const ALL_TOPICS_ENDPOINT = DEPLOY + "/all_topics";
export const USER_TOPICS_ENDPOINT = DEPLOY + "/user_topics";
export const STATISTIC_GENERAL_ENDPOINT = DEPLOY + "/statistic/general";
export const UPVOTE_RATIO_ENDPOINT = DEPLOY + "/statistic/upvote_ratio";
export const STATISTIC_COMMENTS_ENDPOINT = DEPLOY + "/statistic_comments";
export const STATISTIC_UPS_DOWNS_ENDPOINT = DEPLOY + "/statistic_ups_downs";
export const STATISTIC_DOWNS = DEPLOY + "/statistic/downs";
export const CHECK_COMMENTS_ENDPOINT = DEPLOY + "/check_comments";
export const TOP_POSTS_ENDPOINT = DEPLOY + "/last_posts";
export const UPDATE_USER_ENDPOINT = DEPLOY + "/update_user";

export const ADMIN_SEARCH_USER = DEPLOY + "/admin_get_users";
export const ADMIN_ADD_ADMIN = DEPLOY + "/admin_add_admin";
export const ADMIN_REMOVE_ADMIN = DEPLOY + "/admin_remove_admin";
export const ADMIN_REMOVE_USER = DEPLOY + "/admin_remove_user";
export const ADMIN_REMOVE_TOPIC = DEPLOY + "/admin_remove_topic";
export const ADMIN_ADD_TOPIC = DEPLOY + "/admin_add_topic";

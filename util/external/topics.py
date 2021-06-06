from services.server.database.models.topic_model import TopicModel

topics = TopicModel.get_all_topic_names()


def update_topics():
    global topics
    topics = TopicModel.get_all_topic_names()

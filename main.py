from utils import check_update, render_message_text, broadcast

if __name__ == "__main__":
    for school_name, news_list in check_update().items():
        for news in news_list:
            # Replace broadcast() in production.
            broadcast(render_message_text(news, school_name))

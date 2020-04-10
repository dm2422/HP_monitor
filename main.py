from utils import check_update, render_message_text

for name, news_list in check_update().items():
    for news in news_list:
        # Replace broadcast() in production.
        print(render_message_text(news, name))

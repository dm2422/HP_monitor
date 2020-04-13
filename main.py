from API import line_api
from API.twitter_api import twitter_api
from utils import check_update, render_message_text

if __name__ == "__main__":
    for school_name, news_list in check_update().items():
        for news in news_list:
            rendered_text = render_message_text(news, school_name)
            line_api.broadcast(rendered_text)
            twitter_api.update_status(rendered_text)

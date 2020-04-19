from API import line_api, twitter_api
from utils import check_update, initialize_logger

if __name__ == "__main__":
    initialize_logger()

    for school_name, news_list in check_update().items():
        for news in news_list:
            line_api.broadcast(news, school_name)
            twitter_api.broadcast(news, school_name)

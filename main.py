def initialize_logger():
    import logging
    logging.basicConfig(
        level=logging.DEBUG if __debug__ else logging.INFO,
        format="%(asctime)s | %(levelname)s:%(name)s:%(message)s"
    )
    logging.debug("The logger has been initialized.")


if __name__ == "__main__":
    initialize_logger()

    from API.service import line, twitter
    from utils import check_update

    for school_name, news_list in check_update().items():
        for news in news_list:
            line.broadcast(news, school_name)
            twitter.broadcast(news, school_name)

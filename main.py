def initialize_logger():
    import logging
    logging.basicConfig(
        level=logging.DEBUG if __debug__ else logging.INFO,
        format="%(asctime)s | %(levelname)s:%(name)s:%(message)s"
    )
    logging.debug("The logger has been initialized.")


if __name__ == "__main__":
    initialize_logger()

    from shortcuts import check_update, broadcast_all

    for news in check_update():
        broadcast_all(news)

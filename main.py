from utils import initialize_logger, validate_history

if __name__ == "__main__":
    initialize_logger()
    validate_history()

    from shortcuts import check_update, broadcast_all

    for news in check_update():
        broadcast_all(news)

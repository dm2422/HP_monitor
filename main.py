from utils import initialize_logger

if __name__ == "__main__":
    initialize_logger()

    from shortcuts import check_update, broadcast_all

    for news in check_update():
        broadcast_all(news)

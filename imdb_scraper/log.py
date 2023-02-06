import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def log_info(msg: str) -> None:
    logging.info(msg)
    # print(msg)


def log_error(msg: str) -> None:
    logging.error(msg)
    # print(msg)

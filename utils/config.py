import logging

def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app.log",
        filemode="a",
        encoding="UTF-8",
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)-15s:%(lineno)d %(levelname)-7s - %(message)s",

    )
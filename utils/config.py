import logging

log_format = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(module)-15s:%(lineno)-3d %(levelname)-7s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
)
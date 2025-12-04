import sys

from loguru import logger

logger.add(
    sys.stderr,
    format=(
        "[<blue>{time:MMMM D, YYYY -> HH:mm:ss}</blue>] >> "
        "<level>{level: <8}</level>: "
        "<level>{message}</level>"
    ),
    colorize=True,
)

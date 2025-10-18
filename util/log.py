import sys

from loguru import logger

logger.remove(0)
logger.add(
    sys.stderr,
    format=(
        "[<blue>{time:MMMM D, YYYY -> HH:mm:ss}</blue>] >> "
        "<level>{level: <8}</level>: "
        "<level>{message}</level>"
    ),
    colorize=True,
)

# logger.debug("This is a debug message.")
# logger.info("A user updated some information.")
# logger.success("Operation completed successfully!")
# logger.warning("The disk is almost full.")
# logger.error("An error has occurred.")
# logger.critical("Critical failure!")

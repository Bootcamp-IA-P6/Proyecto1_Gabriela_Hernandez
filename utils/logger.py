import logging
import os

def setup_logger():
    """
    Configure and return the main logger for the taximeter app using basicConfig().
    """

    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.basicConfig(
        filename="logs/taximeter.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    logger = logging.getLogger("taximeter")
    return logger

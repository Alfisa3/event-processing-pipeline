import logging
from pathlib import Path


def setup_logger():
    log_directory = Path("data/logs")
    log_directory.mkdir(parents=True, exist_ok=True)

    log_file = log_directory / "pipeline.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger("event_pipeline")


if __name__ == "__main__":
    logger = setup_logger()

    logger.info("Logger started successfully")
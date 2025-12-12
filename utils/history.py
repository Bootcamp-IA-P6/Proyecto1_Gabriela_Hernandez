import os
from datetime import datetime

HISTORY_PATH = "data/trips.txt"


def _ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")


def save_trip(stopped_time, moving_time, total_fare, logger=None):
    """
    Guarda un registro de un trayecto en un archivo de texto plano.
    Formato de línea de ejemplo:
    2025-12-11 15:32:01 | stopped=10.0s | moving=25.0s | total=1.55€
    """
    _ensure_data_dir()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"{timestamp} | "
        f"stopped={stopped_time:.1f}s | "
        f"moving={moving_time:.1f}s | "
        f"total={total_fare:.2f}€\n"
    )

    try:
        with open(HISTORY_PATH, "a", encoding="utf-8") as f:
            f.write(line)

        if logger:
            logger.info("Trip saved to history: %s", line.strip())
    except Exception as e:
        if logger:
            logger.error("Error saving trip to history: %s", e)

import json
import os

DATA_DIR = "data"
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")

DEFAULT_CONFIG = {
    "stopped_rate": 0.02,
    "moving_rate": 0.05,
}


def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_config(logger=None):
    """
    Carga la configuración de precios desde data/config.json.
    Si el archivo no existe o es inválido, crea/usa la configuración por defecto.
    """
    _ensure_data_dir()

    if not os.path.exists(CONFIG_PATH):
        if logger:
            logger.info("Config file not found. Creating default config.")
        save_config(DEFAULT_CONFIG, logger=logger)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        for key, default_value in DEFAULT_CONFIG.items():
            value = config.get(key, default_value)
            if not isinstance(value, (int, float)) or value <= 0:
                if logger:
                    logger.warning(
                        "Invalid value for %s in config. Using default %s.",
                        key,
                        default_value,
                    )
                config[key] = default_value

        return config
    except Exception as e:
        if logger:
            logger.error("Error loading config.json: %s. Using defaults.", e)
        return DEFAULT_CONFIG.copy()


def save_config(config, logger=None):
    """
    Guarda la configuración actual en data/config.json.
    """
    _ensure_data_dir()

    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        if logger:
            logger.info("Pricing configuration saved: %s", config)
    except Exception as e:
        if logger:
            logger.error("Error saving config.json: %s", e)

import time


class Trip:
    """
    Encapsula el estado y la medición de tiempos de un trayecto.

    Maneja:
    - estado actual: 'stopped' o 'moving'
    - acumulados: stopped_seconds, moving_seconds
    - cuándo empezó el estado actual: state_started_at
    """

    def __init__(self):
        self.active = False
        self.state = None
        self.state_started_at = None
        self.stopped_seconds = 0.0
        self.moving_seconds = 0.0

    def start(self):
        if self.active:
            raise RuntimeError("Trip already active")

        self.active = True
        self.stopped_seconds = 0.0
        self.moving_seconds = 0.0
        self.state = "stopped"
        self.state_started_at = time.time()

    def change_state(self, new_state: str):
        if not self.active:
            raise RuntimeError("No active trip")

        if new_state not in ("stopped", "moving"):
            raise ValueError("Invalid state")

        # acumula el tiempo del estado anterior
        now = time.time()
        duration = now - self.state_started_at

        if self.state == "stopped":
            self.stopped_seconds += duration
        elif self.state == "moving":
            self.moving_seconds += duration
        
        self.state = new_state
        self.state_started_at = now

    def finish(self):
        if not self.active:
            raise RuntimeError("No active trip")

        self.change_state(self.state)

        self.active = False
        self.state = None
        self.state_started_at = None

        return self.stopped_seconds, self.moving_seconds

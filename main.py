import time
from utils.logger import setup_logger
from utils.config import load_config, save_config
from utils.history import save_trip
from core.trip import Trip
from infra.trip_repository_db import TripRepositoryDB


logger = setup_logger()
config = load_config(logger=logger)
trip_repo = TripRepositoryDB()


STOPPED_RATE = config["stopped_rate"]
MOVING_RATE = config["moving_rate"]

def calculate_fare(seconds_stopped, seconds_moving):
    """
    Funcion para calcular la tarifa total en euros 
    stopped_rate: €/s
    moving_rate: €/s
    """
    fare = seconds_stopped *STOPPED_RATE + seconds_moving * MOVING_RATE

    logger.info(
        "Calculating fare | stopped=%.1fs, moving=%.1fs, "
        "stopped_rate=%.3f, moving_rate=%.3f, total=%.2f€",
        seconds_stopped,
        seconds_moving,
        STOPPED_RATE,
        MOVING_RATE,
        fare,
    )
    print(f"Este es el total:{fare}")
    return fare 
        
def configure_prices():
    """
    Permite configurar las tarifas desde la CLI y guardarlas en config.json
    """
    global STOPPED_RATE, MOVING_RATE, config

    print("\n--- Pricing configuration ---")
    print(f"Current stopped rate: {STOPPED_RATE} €/s")
    print(f"Current moving rate:  {MOVING_RATE} €/s")

    new_stopped = input("New stopped rate (€/s) [Enter to keep current]: ").strip()
    new_moving = input("New moving rate (€/s)  [Enter to keep current]: ").strip()

    try:
        if new_stopped:
            STOPPED_RATE = float(new_stopped.replace(",", "."))
        if new_moving:
            MOVING_RATE = float(new_moving.replace(",", "."))

        config["stopped_rate"] = STOPPED_RATE
        config["moving_rate"] = MOVING_RATE

        save_config(config, logger=logger)

        print("\n✅ Prices updated successfully.")
        print(f"Stopped: {STOPPED_RATE} €/s | Moving: {MOVING_RATE} €/s\n")

        logger.info(
            "Pricing updated by user | stopped_rate=%.3f, moving_rate=%.3f",
            STOPPED_RATE,
            MOVING_RATE,
        )

    except ValueError:
        print("❌ Invalid input. Prices were not changed.")
        logger.warning("Invalid pricing values entered by user.")


def taximeter():
    """
    Funcion para manejar y mostrar las opciones del taximetro
    """
    print("Welcome to F5 taximeter")
    print(f"available commands:  'start', 'stop', 'move', 'finish', 'exit'\n")

    logger.info("Program started. Waiting for commands")

    trip = Trip()

    while True:
        command = input("> ").strip().lower()
        logger.info(f"Command received : {command}")

        if command == "start":
            try:
                trip.start()
                print("trip started.initial state: 'stopped'")
                logger.info("Trip started. Initial state: stopped.")
            except RuntimeError:
                print("Error:a trip is already in progress")
                logger.warning("User tried to start a trip while another was active")
                continue
             

        elif command in ("stop", "move"):
            new_state = "stopped" if command == "stop" else "moving"
            try:
                trip.change_state(new_state)
                print(f"state change to '{new_state}'.")
                logger.info(
                 "State changed to %s | stopped=%.1fs, moving=%.1fs",
                    new_state,
                    trip.stopped_seconds,
                    trip.moving_seconds,
                )
            except RuntimeError:
                print("error: No activate trip.Please start first")
                logger.warning("User tried to change state without an active trip.")
                continue 


        elif command == "finish": 
            try:
                stopped_time, moving_time = trip.finish()
            except RuntimeError:
                print("Error: no active trip to finish")
                logger.warning("User tried to finish a trip with no active trip.")
                continue
           
            total_fare = calculate_fare(stopped_time, moving_time)

            print("\n--- Trip Summary ---")
            print(f"Stopped time: {stopped_time:.1f} seconds")
            print(f"Moving time: {moving_time:.1f} seconds")
            print(f"Total fare: €{total_fare:.2f}")
            print("---------------------\n")

            logger.info(
                "Trip finished | stopped=%.1fs, moving=%.1fs, total=%.2f€",
                stopped_time,
                moving_time,
                total_fare,
            )

            trip_repo.save_trip(
            stopped_time,
            moving_time,
            STOPPED_RATE,
            MOVING_RATE,
            total_fare
            )
            logger.info("Trip saved to database successfully.")


            save_trip(stopped_time, moving_time, total_fare, logger=logger)
                           
        elif command == "prices":
            configure_prices()

        elif command == "exit":
            print("exiting the program. Goodbye")
            logger.info("Program exiting by user command 'exit'.")
            break

        else: 
            print("unknown command. Use: start, stop, move, finish or exit")
            logger.warning(f"Unknown command received: {command}")

if __name__ == "__main__": 
    taximeter()

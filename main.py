import time
from utils.logger import setup_logger
from utils.config import load_config, save_config

logger = setup_logger()
config = load_config(logger=logger)

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
        f"Calculating fare | stopped={seconds_stopped:.1f}s, "
        f"moving={seconds_moving:.1f}s, "
        f"stopped_rate={STOPPED_RATE}, moving_rate={MOVING_RATE}, total={fare:.2f}€"
    )
    return fare 
        print(f"Este es el total:{fare}")


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

    trip_activate = False    
    stopped_time = 0
    moving_time = 0 
    state = None
    state_start_time = 0 

    while True:
        command = input("> ").strip().lower()
        logger.info(f"Command received : {command}")

        if command == "start":
            if trip_activate:
                print("Error:a trip is already in progress")
                logger.warning("User tried to start a trip while another was active")
                continue

            trip_activate = True            
            stopped_time = 0 
            moving_time = 0 
            state = "stopped"
            state_start_time = time.time()
            

            print("trip started.initial state: 'stopped'")
            logger.info("Trip started. Initial state: stopped.")

        elif command in ("stop", "move"):
            if not trip_activate:
                print("error: No activate trip.Please start first")
                logger.warning("User tried to change state without an active trip.")
                continue 

            duration = time.time()- state_start_time

            if state == "stopped":
                stopped_time += duration
            else: 
                moving_time += duration 
                
            state = "stopped" if command == "stop" else "moving"
            state_start_time = time.time()

            print(f"state change to '{state}'.")
            logger.info(
                f"State change to '{state}'."
                f"Accumulated stopped={stopped_time:.1f}s, moving={moving_time:.1f}s"
            )

        elif command == "finish": 
            if not trip_activate:
                print("Error: no active trip to finish")
                logger.warning("User tried to finish a trip with no active trip.")
                continue

            duration = time.time() - state_start_time

            if state == "stopped":
                stopped_time += duration
            else:
                moving_time += duration

            total_fare = calculate_fare(stopped_time, moving_time)

            print("\n--- Trip Summary ---")
            print(f"Stopped time: {stopped_time:.1f} seconds")
            print(f"Moving time: {moving_time:.1f} seconds")
            print(f"Total fare: €{total_fare:.2f}")
            print("---------------------\n")

            logger.info(
                f"Trip finished. Stopped={stopped_time:.1f}s, "
                f"Moving={moving_time:.1f}s, Total={total_fare:.2f}€"
            )
                
            trip_activate = False
            state = None

        elif command == "prices":
            configure_prices()

        elif command == "exit":
            print("exiting the program, goodbye")
            logger.info("Program exiting by user command 'exit'.")
            break

        else: 
            print("unknown command. Use: start, stop, move, finish or exit")
            logger.warning(f"Unknown command received: {command}")

if __name__ == "__main__": 
    taximeter()

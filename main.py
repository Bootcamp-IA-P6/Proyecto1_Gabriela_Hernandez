import time
from utils.logger import setup_logger

logger = setup_logger()

def calculate_fare(seconds_stopped, seconds_moving):
    """
    Funcion para calcular la tarifa total en euros 
    stopped: 0.02 €/s
    Mooving: 0.05 €/s
    """
    fare = seconds_stopped *0.02 + seconds_moving * 0.05
    print(f"Este es el total:{fare}")
    return fare 

def taximeter():
    """
    Funcion para manejar y mostrar las opciones del taximetro
    """
    print("Welcome to F5 taximeter")
    print(f"available commands:  'start', 'stop', 'move', 'finish', 'exit'\n")

    logger.info("Program started. Waiting for commands")

    trip_activate = False
    start_time = 0
    stopped_time = 0
    moving_time = 0 
    state = None
    state_start_time = 0 

    while True:
        command = input("> ").strip().lower()
        logger.info(f"Command recieved : {command}")

        if command == "start":
            if trip_activate:
                print("Error:a trip is already in progress")
                logger.warning("User tried to start a trip while another was active")
                continue

            trip_activate = True
            start_time = time.time()
            stopped_time = 0 
            moving_time = 0 
            state = "stopped"
            state_start_time = 0
            print("trip started.initial state: 'stopped'")

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

        elif command == "exit":
            print("exiting the program, goodbye")
            logger.info("Program exiting by user command 'exit'.")
            break

        else: 
            print("unknown command. Use: start, stop, move, finish or exit")
            logger.warning(f"Unknown command received: {command}")

if __name__ == "__main__": 
    taximeter()

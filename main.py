import time

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
    trip_activate = False
    start_time = 0
    stopped_time = 0
    moving_time = 0 
    state = None
    state_start_time = 0 

    while True:
        command = input("> ").strip().lower()

        if command == "start":
            if trip_activate:
                print("Error:a trip is already in progress")
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
                continue 

            duration = time.time()- state_start_time

            if state == "stopped":
                stopped_time += duration
            else: 
                moving_time += duration 
                
            state = "stopped" if command == "stop" else "moving"
            state_start_time = time.time()
            print(f"state change to '{state}'.")

        elif command == "finish": 
            if not trip_activate:
                print("Error: no active trip to finish")
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
                
            trip_activate = False
            state = None

        elif command == "exit":
            print("exiting the program, goodbye")
            break

        else: 
            print("unknown command. Use: start, stop, move, finish or exit")

if __name__ == "__main__": 
    taximeter()

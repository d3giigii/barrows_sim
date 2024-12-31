import random
import statistics
import time

from argparse import ArgumentParser, BooleanOptionalAction

# P(N) = 1 / (450 - 58N))
# https://oldschool.runescape.wiki/w/Chest_(Barrows)#Reward_mechanics
drop_chances = {
    1: 392,
    2: 334,
    3: 276,
    4: 218,
    5: 160,
    6: 102
}

def verbose_print(verbose_mode, string):
    if verbose_mode:
        print(string)

def main(args):
    # Handle input.
    num_iterations = getattr(args, "n")
    starting_drops = getattr(args, "s")
    bros_killed = getattr(args, "b")
    verbose_mode = getattr(args, "v")

    # Error handling.
    if num_iterations <= 0:
        raise ValueError("Number of iterations must be at least 1.")
    if starting_drops < 0:
        raise ValueError("Starting drops must be at least 0.")
    if bros_killed < 1 or bros_killed > 6:
        raise ValueError("Brothers killed must be between 1 and 6 inclusive.")

    # Constants.
    num_rolls = 1 + bros_killed
    drop_chance = drop_chances[bros_killed]

    # Simulation variables.
    iteration_results = []
    increment = num_iterations // 10

    # Start the timer.
    start_time = time.time()

    print(f"Begin simulation. Iterations: {num_iterations}")
    verbose_print(verbose_mode, f"Starting Drops: {starting_drops}")
    verbose_print(verbose_mode, f"Brothers Killed: {bros_killed}")

    for iteration in range(num_iterations):

        # New log for each iteration.
        chests = 0
        received_items = [1] * starting_drops + [0] * (24 - starting_drops)

        # One iteration of searching for all barrows uniques.
        while 0 in received_items:

            # Determine if Barrows unique is dropped.
            for _ in range(num_rolls):

                # Using a set would be more appropriate, but
                # iterating over it later leads to ~19% decrease
                # in performance
                chosen_indices = []
                drop_received = random.randint(1, drop_chance) == 1

                if drop_received:

                    # Identical items cannot be given from the same chest.
                    chosen_item_index = random.randint(0, len(received_items) - 1)
                    while chosen_item_index in chosen_indices:

                        # Assumed that duplicate items are re-rolled randomly.
                        chosen_item_index = random.randint(0, len(received_items) - 1)

                    chosen_indices.append(chosen_item_index)

                # Track received items.
                for index in chosen_indices:
                    received_items[index] += 1

            chests += 1

        # Track how many chests it took to receive all items.
        iteration_results.append(chests)

        # Display progress to user.
        if (iteration + 1) % increment == 0:
            print(f"{(iteration + 1) // increment * 10}%", end='\r')

    # Calculate simulation results.
    end_time = time.time()
    mean_chests = statistics.mean(iteration_results)

    # Display simulation results.
    print(f"Simulation Complete. Time: {round(end_time - start_time, 2)}")
    print(f"Mean: {mean_chests}")

    # Write result to output file.
    with open("barrows_results.txt", "+a", encoding="utf-8") as file:
        output = f"{str(num_iterations)},{str(bros_killed)},"
        output += f"{str(starting_drops)},{str(mean_chests)}"
        file.write(output + "\n")

if __name__ == "__main__":

    # Setup input arguments.
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-n", type=int, help="Num. Iterations",
                            default=1000)
    arg_parser.add_argument("-s", type=int, help="Starting Items",
                            default=0)
    arg_parser.add_argument("-b", type=int, help="Brothers Killed",
                            default=6)
    arg_parser.add_argument("-v", type=bool, help="Enable verbose",
                            default=False,
                            action=BooleanOptionalAction)
    input_args = arg_parser.parse_args()

    main(input_args)

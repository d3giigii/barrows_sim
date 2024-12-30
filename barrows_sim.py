import random
import statistics
import time

# Constants. 
bros_killed = 6
num_rolls = 1 + bros_killed
drop_chance = 102 # P(N) = 1 / (450 - 58N)) = 1 / 102
starting_drops = 0

# Simulation variables. 
iteration_results = []
num_iterations = 1000
increment = num_iterations // 10

# Start the timer. 
start_time = time.time()

print(f"Begin simulation. Iterations: {num_iterations}")

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
with open("barrows_results.txt", "+a") as file:
    output = f"{str(num_iterations)},{str(starting_drops)},{str(mean_chests)}"
    file.write(output + "\n")


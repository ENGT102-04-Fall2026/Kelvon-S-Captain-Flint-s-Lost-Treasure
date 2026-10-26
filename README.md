# Captain-Flint-s-Lost-Treasure
A Python program that guides a rover to find Flint's Lost Treasure.
Pseudocode:
Start Program
Setup
Have x = 0, y = 0, depth = 2.0
Set energy = 100.0, set hull = 100.0
Clues = 0, total_time = 0.00
Load mission map from "data/mission_training.csv'
   Set mission_active = True
  
Main loop while mission_active is True:
      Ask pilot for direction (Forward, Backward, Left, Right)
      Calculate new (x, y) coordinates

  IF new position is outside grid:
          Show boundary error message
          Go back to start of loop 
The ELSE function:
Get new depth, distance, and time from map
Calculate hull loss and energy loss
Update x, y, energy, hull, and total time
Update graph plot

CHECK FAILURE: 
IF energy <= 10 OR hull <= 10:
    Print "Mission Failed"
    Stop program

SEARCH LOCATION:
Ask pilot: "Search this location? (yes/no)"
IF pilot says "yes":
    IF location already in searched_list:
      Print "Already searched"
ELSE:
  Add location to searched_list
  Look up category in CSV map
  IF category is "Treasure":
  Print "Success! Treasure Found!"
  Stop program
ELSE:
Apply hull, energy, and clue changes from dictionary
Update plot

IF energy <= 10 OR hull <= 10:
  Print "Mission Failed"
  Stop program
ELSE IF clues >= 6:
  Print "Success! Clue target reached!"
  Stop program

 END
   Print final stats (location, time, energy, hull, clues)
   Save plot image to "plots/mission_plot.png"
END PROGRAM

Rover inputs and state (UPDATE)
Starting variables, x=0, y=0, depth=2, energy=100, hull=100, clues=0, total time=0
Use the function print() in order to print out all the stats and the clue goal when the program starts running.
Make a print asking the user for a movement input, so in the y and x direction (x,y)
Make a counter for time, so time_min+=1
The formulas for hull loss and energy loss:
hull_loss=abs(new_depth - prev_depth) * 0.8 * time_min
energy_loss = (abs(new_depth - prev_depth) * 0.5) + ((distance_m/ time_min) * 1.2) 
POTENTIAL CHALLENGES:
Need to make sure that "time_min is greater than 0 to make the formulas mathematically valid when reading the CSV file
Need to make it able to move in 4 directions along the x and y axes

Engineering notebook design update 4: 
Objective: 
This module loads spatial mission data from mission_training.csv into a coordinate grid to drive an interactive rover navigation loop. It processes user movement inputs to update operational telemetry—such as energy, hull health, and elapsed time—based on depth differentials and speed. It also includes an interactive search prompt that uses a clue/hazard dictionary (SEARCH_EFFECTS) to apply penalties, track clue progress, or trigger victory when the player finds the primary objective.
Progress:
The script successfully parses mission_training.csv to map coordinate data into a localized grid dictionary containing depth, distance, and time metrics. It establishes a 12-turn interactive navigation loop that tracks key telemetry—such as energy, hull integrity, time, and clue points—while applying physics penalties for speed and depth changes. Additionally, it integrates a search system using the SEARCH_EFFECTS dictionary to apply health penalties, accumulate clue progress, and handle win or loss conditions.
Testing evidence: 
Turn 1
Status: Position: (0, 0), Energy: 100, Hull: 100, Time: 0 mins
Direction [F, B, L, R]: f
Position: 0 1
Search this spot? (y/n): y
Found [Low Hazard]: 'Thin weeds brush the rover frame'
Turn 2
Status: Position: (0, 1), Energy: 89.47272727272727, Hull: 93.592, Time: 2.2 mins
Direction [F, B, L, R]: r
Position: 1 1
Search this spot? (y/n): y
Found [None]: 'The search area contains ordinary gravel and silt'
Turn 3
Status: Position: (1, 1), Energy: 78.20508021390374, Hull: 90.98, Time: 4.75 mins
Direction [F, B, L, R]: f
Position: 1 2
Search this spot? (y/n): y
Found [None]: 'No mission evidence is visible at this location'
Turn 4
Status: Position: (1, 2), Energy: 66.39508021390374, Hull: 88.38000000000001, Time: 6.25 mins
Direction [F, B, L, R]: r
Position: 2 2
Search this spot? (y/n): y
Found [Low Hazard]: 'A mild current pushes across the search lane'
Challenges: 
The primary challenge involves boundary check indexing, where comparing movement to num_cols (max_x + 1) rather than max_x allows the rover to step out of bounds and trigger a KeyError. Furthermore, invalid directional inputs and out-of-bounds attempts still advance the turn state without cleanly resetting the loop step. Addressing these logic gaps requires stricter coordinate checks and immediate turn skips on invalid user actions.
Next Steps:
Future work will focus on refactoring the boundary validation conditions (>= num_cols) to completely prevent out-of-bounds matrix errors. Once grid movement is fully stabilized, the team will implement matplotlib.pyplot visualizer functions to plot energy and hull decay across time history. As well as making a program that can provide optimal routes to preserve energy

Week 9 Program Update:
import csv
import matplotlib.pyplot as plt

SEARCH_EFFECTS = {
    "Low Hazard": (-5.0, -5.0, 0),
    "Medium Hazard": (-10.0, -5.0, 0),
    "High Hazard": (-15.0, -10.0, 0),
    "Low Value Clue": (-5.0, -5.0, 1),
    "Strong Clue": (-2.0, -5.0, 2),
    "High Value Clue": (-2.0, -2.0, 3),
    "None": (-2.0, -5.0, 0),
    "Treasure": (0, 0, "immediate success"),
}
grid = {}
max_x = 0
max_y = 0

with open("mission_training.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        if not row:
            continue
        gx = int(row[0])
        gy = int(row[1])
        grid[(gx, gy)]= {
           "at_location": row[2],
            "description": row[3],
            "depth_m": float(row[4]),
            "distance_m": float(row[5]),
            "time_min": float(row[6]),
        }
        if gx > max_x:
            max_x = gx
        if gy > max_y:
            max_y = gy
            
num_cols = max_x + 1
num_rows = max_y + 1


x = 0
y = 0
start_depth_m = 2
depth = grid[(x, y)]["depth_m"]
energy = 100
hull = 100
total_time= 0
clue = 0
clue_target = 6
Failure_Threshold= 10

searched = []
time_history = [0]
energy_history = [100]
hull_history = [100]
depth_history = [depth]
energy_loss_history = [0]
hull_loss_history = [0]
clue_history = [clue]
game_over = False
outcome = "Trip completed (Max turns reached)"

print("Autonomous Underwater Rover Mission Simulation")

for turn in range(12):
    if game_over: 
        break
    
    print(f"Turn {turn + 1}")
    print(f"Status: Position: ({x}, {y}), Energy: {energy}%, Hull: {hull}%, Clues: {clue}/{clue_target} Time: {total_time} mins, Depth: {depth}m")
    
    direction = input("Direction [F, B, L, R]: ").lower()
    
    new_x = x
    new_y = y
    
    if direction == "f":
        new_y = y + 1
    
    if direction == "b":
        new_y = y - 1
    
    if direction == "l":
        new_x = x - 1
    
    if direction == "r":
        new_x = x + 1
        
    if direction not in ["f", "b", "l", "r"]:
        print("Invalid Input Lost time trying to decide...")
        total_time += 1
        
    if (new_x) < 0 or (new_x) > num_cols:
        print("Outside of Grid! Try again")
        
    elif (new_y) < 0 or (new_y) > num_rows:
        print("Outside of Grid! Try again")
    
    else:
        dest = grid[(new_x, new_y)]
        d_new = dest["depth_m"]
        d_prev = depth
        dist = dest["distance_m"]
        t = dest["time_min"]
        
        if t == 0:
            speed_cost = 0.0
        else:
            speed_cost = (dist / t) * 1.2
        
        hull_loss = abs(d_new - d_prev) * 0.8 * t
        energy_loss = (abs(d_new - d_prev) * 0.5) + speed_cost
        hull -= hull_loss
        
        print("Position:", new_x, new_y)
        x= new_x
        y= new_y
        energy -= energy_loss
        total_time += t
        depth = d_new
        
        time_history.append(total_time)
        energy_history.append(energy)
        hull_history.append(hull)
        depth_history.append(depth)
        clue_history.append(clue)
        energy_loss_history.append(energy_loss)
        hull_loss_history.append(hull_loss)
        
        search = input("Search this spot? (y/n): ").lower().strip()
        if search == "y" or search == "yes":
            if (x,y) in searched:
                print("Location already searched!")
            else:
                searched.append((x, y))
                category = dest["at_location"]
                desc = dest["description"]

                print(f"Found [{category}]: '{desc}'")

                if category == "Treasure":
                    print("SUCCESS: Found Captain Flint's Lost Treasure!")
                    outcome = "Success - Found Captain Flint's Lost Treasure!"
                    game_over = True
                else:
                    h_change, e_change, c_change = SEARCH_EFFECTS.get(category, (0, 0, 0))
                    hull += h_change
                    energy += e_change
                    clue += c_change
                    
                    energy_history[-1] = energy
                    hull_history[-1] = hull
                    clue_history[-1] = clue
    
    if energy <= Failure_Threshold or hull <= Failure_Threshold:
        print("Failure: Rover Enegry or hull dropped to 10% or below!")
        outcome = "Failure - Rover Energy or hull dropped to 10% or below!"
        game_over = True
        
    elif clue >= clue_target:
        print(f"SUCCESS: Target clue score reached ({clue} points)!")
        outcome = f"Success - Target clue score reached ({clue} points)"
        game_over = True
        
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    line1 = ax1.plot(time_history, energy_history, marker='o', color='blue', label='Energy Remaining (%)')
    ax1.set_xlabel("Time (mins)")
    ax1.set_ylabel("Energy Remaining (%)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True)

    ax2 = ax1.twinx()
    line2 = ax2.plot(time_history, hull_history, marker='s', color='red', label='Hull Integrity (%)')
    ax2.set_ylabel("Hull Integrity (%)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')

    plt.title("Mission Status: Energy Remaining and Hull Integrity Over Time")
    plt.tight_layout()
    plt.show()

if not game_over:
    print(f"Trip completed! Mission outcome: {outcome}, Final Coordinate: ({x}, {y}), Final time: {total_time} mins, Remaining Energy: {energy}%, Remaining Hull Intergrity: {hull}%, Total Clues Collected: {clue}, Number of Searched Locations: {len(searched)}")

Engineering Notebook Update 5:
Objective:
The primary objective of this project was to implement the full integrated program flow and tracking for the autonomous underwater rover mission parameters, including energy, hull integrity, depth, total time, and clue accumulation. It also incorporated Matplotlib visualization to plot remaining energy and hull integrity against elapsed mission time on dual y-axes while enforcing strict failure thresholds and success conditions.
Progress: 
The program successfully ingests the mission CSV file into a dictionary structure containing depth, distance, time, and location attributes, dynamically determining grid dimensions without hardcoding. Directional inputs are validated against map boundaries, and dynamic energy and hull losses are computed based on depth differentials and movement speed. Additionally, search tracking prevents duplicate inspections, and termination conditions trigger correctly based on resource depletion or target achievement.
Testing Evidence:
Autonomous Underwater Rover Mission Simulation
Turn 1
Status: Position: (0, 0), Energy: 100%, Hull: 100%, Clues: 0/6 Time: 0 mins, Depth: 2.0m
Direction [F, B, L, R]: F
Position: 0 1
Search this spot? (y/n): y
Found [Low Hazard]: 'Thin weeds brush the rover frame'
Turn 2
Status: Position: (0, 1), Energy: 89.47272727272727%, Hull: 93.592%, Clues: 0/6 Time: 2.2 mins, Depth: 2.8m
Direction [F, B, L, R]: r
Position: 1 1
Search this spot? (y/n): y
Found [None]: 'The search area contains ordinary gravel and silt'
Turn 3
Status: Position: (1, 1), Energy: 78.20508021390374%, Hull: 90.98%, Clues: 0/6 Time: 4.75 mins, Depth: 3.1m
Direction [F, B, L, R]: R
Position: 2 1
Search this spot? (y/n): y
Found [Strong Clue]: 'An engraved anchor plate matches the expedition records'
Turn 4
Status: Position: (2, 1), Energy: 68.86542504148994%, Hull: 86.89200000000001%, Clues: 2/6 Time: 7.65 mins, Depth: 4.0m
Challenges: 
A significant challenge during development was plotting the mission status and creating the right graph. Specifically, configuring dual y-axes to track remaining energy percentage and hull integrity percentage over elapsed mission time required meticulous synchronization of historical data lists and axis tick parameters to ensure a clean, readable, technically accurate visual layout.

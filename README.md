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

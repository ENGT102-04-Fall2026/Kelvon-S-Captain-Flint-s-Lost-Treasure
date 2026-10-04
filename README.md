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

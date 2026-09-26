# Captain-Flint-s-Lost-Treasure
A python program that guides a rover to find Flint's Lost Treasure.
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


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
    

"""    
    1. Create at least 10 cars/vehicles as agents.
    2. Create at least 5 parking spaces as agents.
    3. Create a parking lot model using multigrid.
    4. At each step the car should move and find the parking space. 
    You can decide how the car moves to reach the parking space.
    5. Let the car leave the parking space after 3 to 5 steps.
    6. Store the data on steps using data collector and 
    show how many steps it took the cars to occupy a parking space.
    7. Display this simulation graphically.
    8. Increase or decrease parking spaces and cars and see how it simulates. 
    Provide your reflection on this. 
    9. (Optional) Create an obstacle in the parking lot which can represent trees, 
    use A* algorithm to move the car towards the parking space.
"""

# importing Libraries 
import nest_asyncio
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer 


# nest_asyncio to prevent event loop issues
nest_asyncio.apply()

# List for holding parking spaces
parking_spaces = []

class ParkingSpace(Agent):
    """Creating the ParkingSpace Agent each with a unique ID."""
    def __init__(self, unique_id, model, location):
        super().__init__(unique_id, model)
        self.location = location # The parking space's position on the grid
        self.occupied = False # Determines if the parking space is occupied or not

class Car(Agent):
    """Creating the Car Agent, each with a unique ID"""
    def __init__(self, unique_id, model, location):
        super().__init__(unique_id, model)
        self.location = location # The current position of the car on the grid
        self.steps_taken = 0 # How many steps the car has moved
        self.parking_step = 0 # How many steps the car has been parked
        self.parked = False # Indicates if the car is currently parked, or need to keep searching
        self.steps_to_park = [] # How many steps it took the car to park
        self.current_steps = 0 # Tracks steps for the current attempt to park

    def move(self): 
        """Function to move the car in a random direction and check if it has reached a parking space."""
        possible_steps = [
            (0, 1),  # Move up
            (0, -1), # Move down
            (1, 0),  # Move right
            (-1, 0)  # Move left
        ]

        if not self.parked:
            # Shuffle steps to ensure randomness
            self.random.shuffle(possible_steps)

            for dx, dy in possible_steps:
                new_x = (self.location[0] + dx) % self.model.grid.width
                new_y = (self.location[1] + dy) % self.model.grid.height
                new_pos = (new_x, new_y)

                # Check if the cell is empty
                cell_contents = self.model.grid.get_cell_list_contents([new_pos])
                if not any(isinstance(agent, Car) for agent in cell_contents):
                    # Move to the new position
                    self.model.grid.move_agent(self, new_pos)
                    self.location = new_pos
                    self.steps_taken += 1
                    self.current_steps += 1 
                    break  

            # Check if the car has found an unoccupied parking space
            for agent in self.model.grid.get_cell_list_contents([self.location]):
                if isinstance(agent, ParkingSpace) and not agent.occupied:
                    agent.occupied = True
                    self.parked = True 
                    self.parking_step = 0 # Reset the parking step counter
                    self.steps_to_park.append(self.current_steps) # Save the number of steps it took to park
                    print(f"Agent {agent.unique_id} found a parking spot after {self.current_steps} steps.")
                    break 
                     
        if self.parked:
        # Increment parking step counter
            self.parking_step += 1
            if self.parking_step > self.model.random.randint(3, 6): # Check if the car has been parked for 3-5 steps
                # Leave the parking space
                for agent in self.model.grid.get_cell_list_contents([self.location]): # Check if the car is parked
                    if isinstance(agent, ParkingSpace) and agent.occupied: # Check if the parking space is occupied
                        agent.occupied = False # Mark space as unoccupied
                        break
                    
                self.parked = False # Mark the car as not parked
                self.parking_step = 0 # Reset parking step counter
                self.current_steps = 0 # Reset the current steps counter

    def step(self):
        """Move the truck for one step and increment the steps_taken attribute."""
        # if self.steps_taken < self.model.n_steps:
        self.move()

# ParkingLot Model Class
class ParkingLot(Model):
    """Model class for the Parking Lot Model, which contains the grid and schedule."""
    def __init__(self, width, height, n_cars, n_parking_spaces):
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            agent_reporters={
                "StepsTaken":lambda agent: 
                agent.steps_to_park if isinstance(agent, Car) 
                else None
            }
        )
        self.n_cars = n_cars
        self.n_parking_spaces = n_parking_spaces
        self.running = True 

        # Add parking spaces
        for i in range(n_parking_spaces):
            x, y = self.random.randrange(width), self.random.randrange(height)
            parking_space = ParkingSpace(i, self, location=(x, y))
            self.schedule.add(parking_space)
            self.grid.place_agent(parking_space, (x, y))
            parking_spaces.append(parking_space) # Save parking spaces in a list so cars know if they are parked or not   
            
        # Add cars
        for i in range(n_cars):
            x, y = self.random.randrange(width), self.random.randrange(height)
            car = Car(i + n_parking_spaces , self, location=(x, y))
            while any(isinstance(agent, Car) for agent in self.grid.get_cell_list_contents([(x, y)])):
                # Ensure cars do not start in the same position
                x, y = self.random.randrange(width), self.random.randrange(height)
            self.schedule.add(car) # Add the car to the schedule
            self.grid.place_agent(car, (x, y)) # Place the car on the grid 

    def step(self):
        self.schedule.step() # Activate each agent
        self.datacollector.collect(self) # Collect data after each step

# Visualizing the Model
# Cars = blue circles
# Unoccupied parking spaces = Green
# Occupied parking spaces = Red
def agent_portrayal(agent):
    """"Function to determine how agents are displayed in the visualization."""
    portrayal = {}

    if isinstance(agent, Car):
        portrayal = {"Shape": "circle", "Color": "blue", "Filled": "True", "r": 0.5, "Layer": 1, "Label": agent.unique_id}
    elif isinstance(agent, ParkingSpace):
        portrayal = { 
            "Shape": "rect", 
            # "Color": "green" if not agent.occupied else "red", # and isinstance(agent, Car) is agent.parked
            "Color": "red" if agent.occupied else "green", 
            "Filled": "true", 
            "Layer": 0,
            "w": 1,
            "h": 1
            }
 
    return portrayal

# Create the grid for visualization 10x10 grid for example
canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(ParkingLot, [canvas_element], "Parking Lot Model",
                           {"width": 10, "height": 10, "n_cars": 10, "n_parking_spaces": 5})
server.port = 8521

server.launch() # Trailing whitespace is recommended in PY for compatibility reasons -- Nicklas
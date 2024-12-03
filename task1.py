"""    
    1. Create at least 10 cars/vehicles as agents.
    2. Create at least 5 parking spaces as agents.
    3. Create a parking lot model using multigrid.
    4. At each step the car should move and find the parking space. You can decide how the car moves to reach the parking space.
    5. Let the car leave the parking space after 3 to 5 steps.
    6. Store the data on steps using data collector and show how many steps it took the cars to occupy a parking space.
    7. Display this simulation graphically.
    8. Increase or decrease parking spaces and cars and see how it simulates. Provide your reflection on this.
    9. (Optional) Create an obstacle in the parking lot which can represent trees, use A* algorithm to move the car towards the parking space.
"""

# importing Libraries
import random
import nest_asyncio
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

# nest_asyncio to prevent event loop issues
nest_asyncio.apply()

# Creating the ParkingSpace Agent each with a unique ID
class ParkingSpace(Agent):
    def __init__(self, unique_id, model, location, occupied):
        super().__init__(unique_id, model)
        self.location = location # The parking space's position on the grid
        self.occupied = False # Determines if the parking space is occupied or not

# Creating the Car Agent, each with a unique ID
class Car(Agent):
    def __init__(self, unique_id, model, location):
        super().__init__(unique_id, model)
        self.location = location # The current position of the car on the grid
        self.steps_taken = 0 # How many steps the car has moved
        self.parking_step = 0
        self.parked = False # Indicates if the car is currently parked, or need to keep searching

    
    def move(self):
        # An array containing all the possible steps
        possible_steps = [
            (0, 1),  # Move up
            (0, -1), # Move down
            (1, 0),  # Move right
            (-1, 0)  # Move left
        ]

        # Choose a random direction to move
        dx, dy = self.random.choice(possible_steps)
        new_x = (self.location[0] + dx) % self.model.grid.width # wrap around horizontally
        new_y = (self.location[1] + dy) % self.model.grid.height # wrap around vertically
        
        self.location = (new_x, new_y)
        self.model.grid.move_agent(self. self.location)
        self.steps_taken += 1
        
    def leave_parking(self):
        self.parked = False
        sel
        self.step()
        
    def step(self):
        if not self.parked:
            self.move()
        else: 
            self.parking_step += 1
            if self.parking_step > self.model.random.randint(3, 6):
                self.leave_parking()

# List for holding parking spaces
parking_locations = []
                
# ParkingLot Model Class
class ParkingLot(Model):
    def __init__(self, width, height, n_cars, n_parking_spaces):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            agent_reporters={"StepsTaken": "steps_taken"}
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

            # spara parkeringsplatser i en lista så bilarna vet om de är parkerade eller inte 
            parking_locations.append(parking_space.location)

            
        # Add cars
        for i in range(n_cars):
            x, y = self.random.randrange(width), self.random.randrange(height)
            car = Car(i , self.n_parking_spaces, self)
            self.schedule.add(car) # Lägg till bilen i schemat
            self.grid.place_agent(car, (x, y)) # Placera bilen i griden

    def step(self):
        self.schedule.step() # Activate each agent
        self.datacollector.collect(self) # Collect data after each step

# Visualizing the Model
# Cars = blue circles
# Unoccupied parking spaces = Green
# Occupied parking spaces = Red
def agent_portrayal(agent):
    portrayal = {}
    
    if isinstance(agent, Car):
        portrayal = {"Shape": "circle", "Color": "blue", "r": 0.7, "Layer": 1}
    elif isinstance(agent, ParkingSpace):
        portrayal = {
            "Shape": "rect", 
            "Color": "green" if not agent.occupied else "red", 
            "Filled": "true", 
            "Layer": 0,
            "w": 0.5,
            "h": 0.5
            }
        
    return portrayal

# Create the grid for visualization 10x10 grid for example
canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(ParkingLot, [canvas_element], "Parking Lot Model",
                           {"width": 10, "height": 10, "n_cars": 10, "n_parking_spaces": 5})
server.port = 8521
server.launch()
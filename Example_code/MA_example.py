import random # Used to randomly choose the direction in which the truck will move during each step.
import nest_asyncio

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

# nest_asyncio to prevent event loop issues
nest_asyncio.apply()

# --- Agent Definitions ---
class Truck(Agent):
    """A truck agent that moves randomly for a given number of steps."""
       
    def __init__(self, unique_id, model, location):
        super().__init__(unique_id, model)
        self.location = location  # Location of the truck on the grid
        self.steps_taken = 0  # Track the number of steps taken

    def move(self):
        """Move the truck randomly in one of four directions (up, down, left, right)."""
        possible_steps = [
            (0, 1),  # Move up
            (0, -1), # Move down
            (1, 0),  # Move right
            (-1, 0)  # Move left
        ]
        
        # Choose a random direction to move
        dx, dy = self.random.choice(possible_steps)
        new_x = (self.location[0] + dx) % self.model.grid.width  # Wrap around horizontally
        new_y = (self.location[1] + dy) % self.model.grid.height  # Wrap around vertically
        
        # Update the truck's location
        self.location = (new_x, new_y)
        self.model.grid.move_agent(self, self.location)
        self.steps_taken += 1  # Increment the steps_taken attribute

    def step(self):
        """Move the truck for one step and increment the steps_taken attribute."""
        if self.steps_taken < self.model.num_steps:
            self.move()

# --- Model Definition ---
class SimpleTruckModel(Model):
    """A simple model where trucks move randomly for a fixed number of steps."""
    
    def __init__(self, width, height, num_trucks, num_steps):
        self.num_agents = num_trucks
        self.grid = MultiGrid(width, height, True)  # Grid environment
        self.schedule = RandomActivation(self)  # Random activation scheduler
        self.num_steps = num_steps  # Number of steps for the simulation
        
        # Create data collectors
        self.datacollector = DataCollector(
            agent_reporters={"StepsTaken": "steps_taken"}
        )

        self.trucks = []
        
        # Create trucks
        for i in range(num_trucks):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            truck = Truck(i, self, location=(x, y))
            self.schedule.add(truck)
            self.grid.place_agent(truck, (x, y))
            self.trucks.append(truck)

    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()

    def run_model(self):
        """Run the model for a fixed number of steps (num_steps)."""
        for i in range(self.num_steps):
            self.step()

# --- Visualization ---
def agent_portrayal(agent):
    """Visual portrayal of agents."""
    portrayal = {}
    
    if isinstance(agent, Truck):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "blue"  # Trucks are blue
        portrayal["r"] = 0.7
        portrayal["Layer"] = 1  # Trucks should appear above the grid cells

    return portrayal

# Create the grid for visualization (10x10 grid for example)
canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# Now we are setting up the server to run the simulation with visualization
def truck_model():
    model = SimpleTruckModel(width=10, height=10, num_trucks=3, num_steps=100)  # 3 trucks, 100 steps
    server = ModularServer(SimpleTruckModel, [canvas_element], "Simple Truck Model",
                           {"width": 10, "height": 10, "num_trucks": 3, "num_steps": 100})
    server.port = 8521
    return server

server = truck_model()

# Launch the server and allow the event loop to start
server.launch()

# After running the simulation
model = SimpleTruckModel(width=10, height=10, num_trucks=3, num_steps=100)
model.run_model()  # Run the model for exactly 100 steps

# Get the data
data = model.datacollector.get_agent_vars_dataframe()
print(data)

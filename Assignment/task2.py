"""
    1. Create 50 tasks with varying duration and resources.

        Example:
            Task 1: Duration = 10 units, Resources = 2 (requires 2 agents to work together).
            Task 2: Duration = 15 units, Resources = 3 (requires 3 agents to work together).
            Task 3: Duration = 17 units, Resources = 1 (requires 1 agent).

    2. Create three agents with maximum capacity of 2. Agents can have a capacity greater than 1 to allow for more flexible task allocation. Agents will be fixed on the grid.
        Example:
            Agent 1 has capacity = 2, meaning it can handle 2 tasks concurrently.
            Agent 2 has capacity = 1, meaning it can handle 1 task at a time.

    3. Create a visualization showing the cooperative task scheduling between multiple agents. 
    For instance, you can show change the colour of agents to similar colour of agents when two or more agents are running one task.

    4. Print cooperation of agents like this
        {"type":"get_step","step":1}
        Agent 3 is working on Task 0, Task Duration: 4
        Agent 4 is working on Task 1, Task Duration: 5
        Agent 1 is working on Task 2, Task Duration: 9
        {"type":"get_step","step":2}
        Agent 1 is working on Task 2, Task Duration: 8
        Agent 3 is working on Task 0, Task Duration: 3
        Agent 4 is working on Task 1, Task Duration: 4
        {"type":"get_step","step":3}
        Agent 1 is working on Task 2, Task Duration: 7
        Agent 4 is working on Task 1, Task Duration: 3
        Agent 3 is working on Task 0, Task Duration: 2
"""
# Importing required libraries
import random
import nest_asyncio
from multiprocessing import Pool, cpu_count
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer 

# nest_asyncio to prevent event loop issues
nest_asyncio.apply()

# Task Class
class Task:
    """Represents a task with a duration and resource requirement."""
    def __init__(self, task_id, duration, resources):
        self.task_id = task_id
        self.duration = duration
        self.resources = resources
        self.remaining_duration = duration  # Tracks task progress

# Worker Agent Class
class WorkerAgent(Agent):
    """An agent that can work on tasks."""
    
class CooperativeTaskModel(Model):
    """A model for cooperative task scheduling."""
    
def agent_portrayal(agent):
    """Determines how agents are displayed in the visualization."""    


    # Visualization
    canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
    
    server = ModularServer(CooperativeTaskModel, [canvas_element], "Cooperative Task Model",
                           {"width": 10, "height": 10, "num_agents": 3, "task_list": generate_tasks()})
    
    server.port = 8521
    
    server.launch()
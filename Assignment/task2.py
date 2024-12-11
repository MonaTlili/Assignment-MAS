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
    def __init__(self, unique_id, model, capacity):
        super().__init__(unique_id, model)
        self.capacity = capacity
        self.current_task = []  # List of tasks being worked on
        
    def step(self):
        """Agent step function."""
        for task in self.current_task[:]: # Update progress of current tasks
            task.remaining_duration -= 1
            if task.remaining_duration == 0:
                self.current_task.remove(task) # Task completed 
                
        while len(self.current_task) < self.capacity and self.model.pending_tasks: # Assign new tasks if the agent has capacity
            new_task = self.model.pending_tasks.pop(0) # Get a new task
            self.current_task.append(new_task) # Assign the task to the agent
            
        for task in self.current_task: # Print task status information
            print(f"Agent {self.unique_id} is working on Task {task.task_id}, Task Duration: {task.remaining_duration}")
           
class CooperativeTaskModel(Model):
    """A model for cooperative task scheduling."""
    def __init__(self, width, height, num_agents, task_list):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.pending_tasks = task_list
        
        self.agents = []
        capacities = [2, 1, 2] # Example capacities for agents, could be [1, 2, 1] or any other combination, with maximum capacity of 2 / agent
        for i in range(num_agents):
            # agent = WorkerAgent(i, self, random.randint(1, 3))
            # x = self.random.randrange(self.grid.width)
            # y = self.random.randrange(self.grid.height)
            # self.grid.place_agent(agent, (x, y))
            agent = WorkerAgent(i, self, capacity=capacities[i])
            self.schedule.add(agent)
            self.agents.append(agent)
            self.grid.place_agent(agent, (i, height // 2))  # Place agents on the grid
            
        self.running = True 
        
    def step(self): 
        print(f'{"-"*10} Step {self.schedule.steps + 1} {"-"*10}')
        self.schedule.step()
        
    
def generate_tasks():
    """Generates a list of tasks with varying duration and resource requirements."""
    tasks = []
    for i in range(50):
        duration = random.randint(5, 20)
        resources = random.randint(1, 3)
        tasks.append(Task(i, duration, resources))
    return tasks
        
def agent_portrayal(agent):
    """Determines how agents are displayed in the visualization."""
    
    portrayal = {"Shape": "circle", "Filled": True, "r": 0.5}
    
    if isinstance(agent, WorkerAgent):
        task_count = len(agent.current_task)
        portrayal["Color"] = "red" if task_count > 1 else "green" if task_count == 1 else "blue"
        portrayal["Layer"] = 1 
        portrayal["Label"] = f"{len(agent.current_task)} tasks"
        
    return portrayal 

# Visualization
canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(CooperativeTaskModel, [canvas_element], "Cooperative Task Model",
                        {"width": 10, "height": 10, "num_agents": 3, "task_list": generate_tasks()})

server.port = 8521

server.launch()
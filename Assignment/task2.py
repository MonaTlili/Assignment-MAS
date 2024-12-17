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

# nest_asyncio to prevent event loop issues, when running the code in environments like Jupyter Notebook
nest_asyncio.apply()

class Task: 
    """Represents a task with a duration and resource requirement."""
    def __init__(self, task_id, duration, resources):
        self.task_id = task_id
        self.duration = duration
        self.resources = resources 
        self.remaining_duration = duration 
        self.assigned_agents = []
        
    # Checks if an agent has completed a task
    def is_complete(self):
        return self.remaining_duration <= 0
    
    # Checks if a task has been assigned enough agents 
    def is_fully_assigned(self):
        return len(self.assigned_agents) == self.resources
    
    # Makes sure that agents are working on their designated task 
    def work_on_task(self):
        if self.is_fully_assigned():
            self.remaining_duration -= 1 

class WorkerAgent(Agent):
    """An agent that can work on tasks."""
    def __init__(self, unique_id, model, capacity):
        super().__init__(unique_id, model)
        self.capacity = capacity 
        self.current_tasks = []
        
    def step(self):
        """ 
        Step function managing the agent's tasks by working on current tasks, removing completed ones and assigning new ones
        Ensures that the resources required for a task are met before starting the task, coordinating with other agents
        Prints the status of the agent's tasks 
        """
        for task in self.current_tasks:
            task.work_on_task()
            if task.is_complete():
                print(f"Task {task.task_id} completed by Agent {self.unique_id}")
                print(f"")
                task.assigned_agents.remove(self.unique_id)
                self.current_tasks.remove(task)

        if len(self.current_tasks) < self.capacity:
            for task in self.model.pending_tasks:
                if self.unique_id in task.assigned_agents or task.is_complete():
                    continue
                if not task.is_fully_assigned() and len(task.assigned_agents) < task.resources:
                    task.assigned_agents.append(self.unique_id)
                    self.current_tasks.append(task)
                    print(f"Agent {self.unique_id} assigned to Task {task.task_id}")
                    print(f"")
                    break

        for task in self.current_tasks:
            if len(task.assigned_agents) < task.resources:
                print(f"Agent {self.unique_id} is waiting at Task {task.task_id} for another resource")
                print(f"")
                continue

            other_agents = [agent_id for agent_id in task.assigned_agents if agent_id != self.unique_id]
            print(
                f"Agent {self.unique_id} is working on Task {task.task_id}, Task duration: {task.duration}, "
                f"{'by itself' if not other_agents else ' with Agent(s): ' + ', '.join(map(str, other_agents))}"
            )
            print(f"")


class CooperativeTaskModel(Model):
    """A model for cooperative task scheduling."""
    def __init__(self, width, height, num_agents, task_list):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.pending_tasks = task_list
        
        self.agents = []
        capacities = [1, 2, 2] 

        if num_agents != len(capacities):
            raise ValueError(f"The number of agents ({num_agents}) does not match the length of the capacities list ({len(capacities)}).")

        for i in range(num_agents):
            agent = WorkerAgent(i, self, capacity=capacities[i])
            self.schedule.add(agent)
            self.agents.append(agent)
            self.grid.place_agent(agent, (i, height // 2))

        self.running = True

    # Step function for the model, which prints the current step and calls the step function of the schedule
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
    """Function to define the portrayal of agents in the visualization."""
    portrayal = {"Shape": "circle", "Filled": True, "r": 0.5}
    
    if isinstance(agent, WorkerAgent):
        active_task_count = sum(1 for task in agent.current_tasks if len(task.assigned_agents) >= task.resources)
        
        if active_task_count > 1:
            portrayal["Color"] = "green"
        elif active_task_count == 1:
            portrayal["Color"] = "yellow"
        else:
            portrayal["Color"] = "gray"
        
        portrayal["Layer"] = 1
        portrayal["Label"] = f"{active_task_count} task{'s' if active_task_count != 1 else ''}"
    
    return portrayal

canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(CooperativeTaskModel, [canvas_element], "Cooperative Task Model",
                       {"width": 10, "height": 10, "num_agents": 3, "task_list": generate_tasks()})

server.port = 8521
server.launch()
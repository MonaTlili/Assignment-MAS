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
import numpy as np 
import time
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# Creating Car Agent
class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    self.parked = False
    self.steps = 0

    def sttep(self):





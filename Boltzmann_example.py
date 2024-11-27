from mesa import Agent

class MoneyAgent(Agent):
    """An agent with fixed initial wealth.

    Each agent starts with 1 unit of wealth and can give 1 unit to other agents
    if they occupy the same cell.

    Attributes:
        wealth (int): The agent's current wealth (starts at 1)
    """

    def __init__(self, model):
        """Create a new agent.

        Args:
            model (Model): The model instance that contains the agent
        """
        super().__init__(model)
        self.wealth = 1

    def move(self):
        """Move the agent to a random neighboring cell."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        """Give 1 unit of wealth to a random agent in the same cell."""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        # Remove self from potential recipients
        cellmates.pop(cellmates.index(self))

        if cellmates:  # Only give money if there are other agents present
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        """Execute one step for the agent:
        1. Move to a neighboring cell
        2. If wealth > 0, maybe give money to another agent in the same cell
        """
        self.move()
        if self.wealth > 0:
            self.give_money()

"""
Boltzmann Wealth Model
=====================

A simple model of wealth distribution based on the Boltzmann-Gibbs distribution.
Agents move randomly on a grid, giving one unit of wealth to a random neighbor
when they occupy the same cell.
"""

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.examples.basic.boltzmann_wealth_model.agents import MoneyAgent
from mesa.space import MultiGrid


class BoltzmannWealth(Model):
    """A simple model of an economy where agents exchange currency at random.

    All agents begin with one unit of currency, and each time step agents can give
    a unit of currency to another agent in the same cell. Over time, this produces
    a highly skewed distribution of wealth.

    Attributes:
        num_agents (int): Number of agents in the model
        grid (MultiGrid): The space in which agents move
        running (bool): Whether the model should continue running
        datacollector (DataCollector): Collects and stores model data
    """

    def __init__(self, n=100, width=10, height=10, seed=None):
        """Initialize the model.

        Args:
            n (int, optional): Number of agents. Defaults to 100.
            width (int, optional): Grid width. Defaults to 10.
            height (int, optional): Grid height. Defaults to 10.
            seed (int, optional): Random seed. Defaults to None.
        """
        super().__init__(seed=seed)

        self.num_agents = n
        self.grid = MultiGrid(width, height, torus=True)

        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={"Gini": self.compute_gini},
            agent_reporters={"Wealth": "wealth"},
        )

        # Create and place the agents
        for _ in range(self.num_agents):
            agent = MoneyAgent(self)

            # Add agent to random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle_do("step")  # Activate all agents in random order
        self.datacollector.collect(self)  # Collect data

    def compute_gini(self):
        """Calculate the Gini coefficient for the model's current wealth distribution.

        The Gini coefficient is a measure of inequality in distributions.
        - A Gini of 0 represents complete equality, where all agents have equal wealth.
        - A Gini of 1 represents maximal inequality, where one agent has all wealth.
        """
        agent_wealths = [agent.wealth for agent in self.agents]
        x = sorted(agent_wealths)
        n = self.num_agents
        # Calculate using the standard formula for Gini coefficient
        b = sum(xi * (n - i) for i, xi in enumerate(x)) / (n * sum(x))
        return 1 + (1 / n) - 2 * b

from mesa.examples.basic.boltzmann_wealth_model.model import BoltzmannWealth
from mesa.visualization import (
    SolaraViz,
    make_plot_component,
    make_space_component,
)


def agent_portrayal(agent):
    color = agent.wealth  # we are using a colormap to translate wealth to color
    return {"color": color}


model_params = {
    "n": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents:",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": 10,
    "height": 10,
}


def post_process(ax):
    ax.get_figure().colorbar(ax.collections[0], label="wealth", ax=ax)


# Create initial model instance
model = BoltzmannWealth(50, 10, 10)

# Create visualization elements. The visualization elements are solara components
# that receive the model instance as a "prop" and display it in a certain way.
# Under the hood these are just classes that receive the model instance.
# You can also author your own visualization elements, which can also be functions
# that receive the model instance and return a valid solara component.

SpaceGraph = make_space_component(
    agent_portrayal, cmap="viridis", vmin=0, vmax=10, post_process=post_process
)
GiniPlot = make_plot_component("Gini")

# Create the SolaraViz page. This will automatically create a server and display the
# visualization elements in a web browser.
# Display it using the following command in the example directory:
# solara run app.py
# It will automatically update and display any changes made to this file
page = SolaraViz(
    model,
    components=[SpaceGraph, GiniPlot],
    model_params=model_params,
    name="Boltzmann Wealth Model",
)
page  # noqa


# In a notebook environment, we can also display the visualization elements directly
# SpaceGraph(model1)
# GiniPlot(model1)

# The plots will be static. If you want to pick up model steps,
# you have to make the model reactive first
# reactive_model = solara.reactive(model1)
# SpaceGraph(reactive_model)
# In a different notebook block:
# reactive_model.value.step()            
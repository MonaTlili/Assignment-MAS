# Assignment-MAS

    Multiagent models represent an abstraction of reality. 
    This can be applied to multiple real-world interactions. 
    Similarly, this can also be applied to distributed computing architecture where multi-agent model can be used to simulate things like bandwidth payload, 
    resource allocation, scheduling, etc. 
    The goal of the assignment is to demonstrate how multi-agent systems (MAS) can be applied to distributed computing.

### Task 1 - Mesa (Obligatory): Non-cooperative or Independent
    1. Create at least 10 cars/vehicles as agents.
    2. Create at least 5 parking spaces as agents.
    3. Create a parking lot model using multigrid.
    4. At each step the car should move and find the parking space. You can decide how the car moves to reach the parking space.
    5. Let the car leave the parking space after 3 to 5 steps.
    6. Store the data on steps using data collector and show how many steps it took the cars to occupy a parking space.
    7. Display this simulation graphically.
    8. Increase or decrease parking spaces and cars and see how it simulates. Provide your reflection on this.
    9. (Optional) Create an obstacle in the parking lot which can represent trees, use A* algorithm to move the car towards the parking space.

### Task 2 – Mesa (For VG): Cooperative task scheduling
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

### Task 3 – Multiprocessing (Obligatory): Count words
    1. Use the textfile named “pg2701”
    2. Split the text file to chunks (group of sentences)
    3. Clean the data and count the words using single and multi-thread
    4. Identify processing times between them
    5. Explain the difference in performance


## Hand-in:
    Finally, write a short reflection with images of your simulation. Maximum of 2 pages.

    Code as notebook or python files

    Presentation: 
        Record a video in which you explain your code and run the results of the above two simulation tasks. 
        Upload this video to YouTube or upload the video file in Canvas. 
        Maximum time of recorded video is 15 minutes. All the persons in the group should be involved in the presentation.
        Deadline: Assignment 1 needs to be submitted no later than Dec/12 23.59 in the submission folder on Canvas/Assignments/Assignment 1.
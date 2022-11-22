from mesa import Agent


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction
        chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.prevSentido = ""

    def move(self):
        """
        Determines if the agent can move in the direction that was chosen
        """
        cord = list(self.pos)
        cordstr = str(cord)
        if cordstr in self.model.dicSentido:
            sentido = self.model.dicSentido[cordstr]
            if sentido == "<":
                nexcord = ((cord[0] - 1), cord[1])
            elif sentido == ">":
                nexcord = ((cord[0] + 1), cord[1])

            elif sentido == "v":
                nexcord = (cord[0], (cord[1] - 1))

            elif sentido == "^":
                nexcord = (cord[0], (cord[1] + 1))

            # print(f'nexcord raro {nexcord}')
            # print(f'Coordenada anterior {cord}')
            self.prevSentido = sentido
            # print(f'El sentido anterior es {self.prevSentido}')
        else:
            # print(f'Seguir hacia  {self.prevSentido}')
            if self.prevSentido == "<":
                nexcord = ((cord[0] - 1), cord[1])
            elif self.prevSentido == ">":
                nexcord = ((cord[0] + 1), cord[1])

            elif self.prevSentido == "v":
                nexcord = (cord[0], (cord[1] - 1))

            elif self.prevSentido == "^":
                nexcord = (cord[0], (cord[1] + 1))

        self.model.grid.move_agent(self, nexcord)

    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        self.move()


class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state=False, timeToChange=10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step
                          should the traffic light change color
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """
        To change the state (green or red) of the traffic light in case
        you consider the time to change of each traffic light.
        """
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass


class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction="Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass

from mesa import Agent
from math import sqrt, pow


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
        self.tipo = "car"
        self.nexcord = ()
        self.destino = None
        self.prevcord = ()


    def move(self):
        """
        Determines if the agent can move in the direction that was chosen
        """
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False,
            radius=1)

        cord = list(self.pos)
        cordstr = str(cord)
        for i in possibleSteps:
            cellmates = self.model.grid.get_cell_list_contents(i)
            for j in cellmates:
                if j.tipo == "destino" and j.pos == self.destino:
                    print("Encontraste destino")
                if j.tipo == "semaforo" and j.state is False:
                    self.nexcord = self.pos
                elif j.tipo == "semaforo" and j.state is True:
                    if self.prevSentido == "<":
                        self.nexcord = ((cord[0] - 1), cord[1])
                    elif self.prevSentido == ">":
                        self.nexcord = ((cord[0] + 1), cord[1])
                    elif self.prevSentido == "v":
                        self.nexcord = (cord[0], (cord[1] - 1))
                    elif self.prevSentido == "^":
                        self.nexcord = (cord[0], (cord[1] + 1))
                elif j.tipo == "calle":
                    if cordstr in self.model.dicSentido:
                        sentido = self.model.dicSentido[cordstr]
                        self.prevSentido = sentido
                        if sentido == "<":
                            self.nexcord = ((cord[0] - 1), cord[1])
                        elif sentido == ">":
                            self.nexcord = ((cord[0] + 1), cord[1])
                        elif sentido == "v":
                            self.nexcord = (cord[0], (cord[1] - 1))
                        elif sentido == "^":
                            self.nexcord = (cord[0], (cord[1] + 1))
                        elif sentido == "c":
                            distanciaActual = 10000000000000000
                            for k in possibleSteps:
                                if k != self.prevcord:  # Evaluo que no sea la posición pasada
                                    cellmates = self.model.grid.\
                                        get_cell_list_contents(k)
                                    for n in cellmates:
                                        if n.tipo == "calle" or n.tipo == "semaforo":
                                            disObjetivo = sqrt(
                                                pow(self.destino[0] - k[0], 2)
                                                + pow((self.destino[1]
                                                        - k[1]), 2))
                                            if distanciaActual > disObjetivo:
                                                sentido2 = self.model.dicSentido[str(list(n.pos))]
                                                val = self.validarmov(sentido2, list(n.pos), cord)
                                                if val:
                                                    print(sentido2)
                                                    distanciaActual = disObjetivo
                                                    Ncord = list(n.pos)
                                # else:
                                #     print(f'Coordenada No valida {k}')
                                #     print(f'sentido {sentido}')
                            self.nexcord = (Ncord[0], Ncord[1])
        self.prevcord = self.pos
        print(f'Coordenada antigua {self.prevcord}')

    def validarmov(self, SCasilla: str, Objetivo: list, Origen: list) -> bool:
        XOrigen = Origen[0]
        YOrigen = Origen[1]
        XObjetivo = Objetivo[0]
        YObjetivo = Objetivo[1]
        if SCasilla == "<":
            if XObjetivo < XOrigen:
                return True
            else:
                return False
        elif SCasilla == ">":
            if XObjetivo > XOrigen:
                return True
            else:
                return False
        elif SCasilla == "v":
            if YOrigen > YObjetivo:
                return True
            else:
                False
        elif SCasilla == "^":
            if YOrigen < YObjetivo:
                return True
            else:
                False
        elif SCasilla == "c":
            return True
        return False

    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        self.move()

    def advance(self) -> None:
        self.model.grid.move_agent(self, self.nexcord)   


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
        self.tipo = "semaforo"

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
        self.tipo = "destino"

    def step(self):
        pass


class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = "edificio"

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
        self.tipo = "calle"

    def step(self):
        pass

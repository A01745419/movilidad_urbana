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
            # print(cellmates)
            # print(type(cellmates))
            for j in cellmates:
                if "car" in cellmates:
                    print("La lista tiene carro")
                if j.tipo == "destino" and j.pos == self.destino:
                    print("Encontraste destino")
                elif j.tipo == "semaforo" and j.state is False:
                    if self.prevSentido == ">":
                        if self.pos == j.pos or self.pos[0] < j.pos[0]\
                             and self.pos[1] == j.pos[1]:
                            self.nexcord = self.pos
                    elif self.prevSentido == "<":
                        if self.pos == j.pos or self.pos[0] > j.pos[0]\
                             and self.pos[1] == j.pos[1]:
                            self.nexcord = self.pos
                    elif self.prevSentido == "^":
                        if self.pos == j.pos or self.pos[1] < j.pos[1]\
                             and self.pos[0] == j.pos[0]:
                            self.nexcord = self.pos
                    elif self.prevSentido == "v":
                        if self.pos == j.pos or self.pos[1] > j.pos[1]\
                             and self.pos[0] == j.pos[0]:
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
                elif j.tipo == "calle" and len(cellmates) == 1:
                    if cordstr in self.model.dicSentido:
                        sentido = self.model.dicSentido[cordstr]
                        self.prevSentido = sentido
                        if sentido == "<":
                            # cambio = self.cambiodecarril(cord, possibleSteps,
                            #                          sentido, self.destino)
                            # if cambio[0]:
                            #     print("CAMBIO CARRIL 1")
                            #     if cambio[1] < 0:
                            #         self.nexcord = (cord[0], (cord[1] + 1))
                            #     else:
                            #         self.nexcord = (cord[0], (cord[1] - 1))
                            # else:
                            self.nexcord = ((cord[0] - 1), cord[1])
                        elif sentido == ">":
                            # cambio = self.cambiodecarril(cord, possibleSteps,
                            #                              sentido, self.destino)
                            # if cambio[0]:
                            #     print("CAMBIO CARRIL 2")
                            #     if cambio[1] < 0:
                            #         self.nexcord = (cord[0], (cord[1] + 1))
                            #     else:
                            #         self.nexcord = (cord[0], (cord[1] - 1))
                            # else:
                            self.nexcord = ((cord[0] + 1), cord[1])
                        elif sentido == "v":
                            # cambio = self.cambiodecarril(cord, possibleSteps,
                            #                              sentido, self.destino)
                            # if cambio[0]:
                            #     print("CAMBIO CARRIL 3")
                            #     if cambio[1] < 0:
                            #         self.nexcord = ((cord[0] - 1), cord[1])
                            #     else:
                            #         self.nexcord = ((cord[0] + 1), cord[1])
                            # else:
                            self.nexcord = (cord[0], (cord[1] - 1))
                        elif sentido == "^":
                            # cambio = self.cambiodecarril(cord, possibleSteps,
                            #                  sentido, self.destino)
                            # if cambio[0]:
                            #     print("CAMBIO CARRIL 4")
                            #     if cambio[1] < 0:
                            #         self.nexcord = ((cord[0] - 1), cord[1])
                            #     else:
                            #         self.nexcord = ((cord[0] + 1), cord[1])
                            # else:
                            self.nexcord = (cord[0], (cord[1] + 1))
                        elif sentido == "c":
                            distanciaActual = 10000000000000000
                            for k in possibleSteps:
                                # Evaluo que no sea la posición pasada
                                if k != self.prevcord:
                                    cellmates = self.model.grid.\
                                        get_cell_list_contents(k)
                                    for n in cellmates:
                                        if n.tipo == "calle" or\
                                             n.tipo == "semaforo":
                                            disObjetivo = self.\
                                                euclidiana(self.destino, k)
                                            if distanciaActual > disObjetivo:
                                                sentido2 = self.model.\
                                                    dicSentido[str(list
                                                               (n.pos))]
                                                val = self.\
                                                    validarmov(sentido2,
                                                               list(n.pos),
                                                               cord)
                                                if val:
                                                    # print(sentido2)
                                                    distanciaActual =\
                                                        disObjetivo
                                                    Ncord = list(n.pos)
                                # else:
                                #     print(f'Coordenada No valida {k}')
                                #     print(f'sentido {sentido}')
                            self.nexcord = (Ncord[0], Ncord[1])
                if j.tipo == "car" and j.pos == self.nexcord:
                    print(f'Encontro carro en la posicion {j.pos} en la casilla a mover el carro {self.pos}')
                    print(self.nexcord)
                    self.nexcord == self.prevcord
                    print(self.nexcord)
        self.prevcord = self.pos
        print(f'Coordenada antigua {self.prevcord} del carro {self.pos}')

    def cambiodecarril(self,
                       CordO: list,
                       PS: list,
                       SCasilla: str,
                       Destino: list) -> list:
        result: list = []
        XOrigen = CordO[0]
        YOrigen = CordO[1]
        for i in PS:
            cellmates = self.model.grid.get_cell_list_contents(i)
            for j in cellmates:
                if SCasilla == "<" and XOrigen == i[0] and YOrigen != i[1] and\
                   j.tipo == "calle":
                    disObjetivo1 = self.euclidiana(Destino, i)
                    disObjetivo2 = self.euclidiana(Destino, CordO)
                    if disObjetivo1 > disObjetivo2:
                        return [False, 0]
                    else:
                        arribaAbajo = YOrigen - i[1]
                        if arribaAbajo < 0:
                            # Mover arriba
                            return [True, 1]
                        else:
                            # Mover abajo
                            return [True, -1]

                elif SCasilla == ">" and XOrigen == i[0] and\
                        YOrigen != i[1] and\
                        j.tipo == "calle":
                    disObjetivo1 = self.euclidiana(Destino, i)
                    disObjetivo2 = self.euclidiana(Destino, CordO)
                    if disObjetivo1 > disObjetivo2:
                        return [False, 0]
                    else:
                        arribaAbajo = YOrigen - i[1]
                        if arribaAbajo < 0:
                            # Mover arriba
                            return [True, 1]
                        else:
                            # Mover abajo
                            return [True, -1]

                elif SCasilla == "v" and YOrigen == i[1] and\
                        XOrigen != i[0] and\
                        j.tipo == "calle":
                    disObjetivo1 = self.euclidiana(Destino, i)
                    disObjetivo2 = self.euclidiana(Destino, CordO)
                    if disObjetivo1 > disObjetivo2:
                        return [False, 0]
                    else:
                        izDer = XOrigen - i[0]
                        if izDer < 0:
                            # Mover derecha
                            return [True, 1]
                        else:
                            # Mover izquierda
                            return [True, -1]

                elif SCasilla == "^" and YOrigen == i[1] and\
                        XOrigen != i[0] and\
                        j.tipo == "calle":
                    disObjetivo1 = self.euclidiana(Destino, i)
                    disObjetivo2 = self.euclidiana(Destino, CordO)
                    if disObjetivo1 > disObjetivo2:
                        return [False, 0]
                    else:
                        izDer = XOrigen - i[0]
                        if izDer < 0:
                            # Mover derecha
                            return [True, 1]
                        else:
                            # Mover izquierda
                            return [True, -1]
        return result

    def euclidiana(self, Edestino: list, Ek: list) -> float:
        return sqrt(pow(Edestino[0] - Ek[0], 2) +
                    pow((Edestino[1] - Ek[1]), 2))

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

    def modificarcolor(self):
        self.compañero = []
        self.vecinos = []

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
        self.usada = False

    def step(self):
        pass

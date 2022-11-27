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
        self.parado = False
        self.mepuedomover = True
        self.entrada = None
        self.NoDestino = True
        self.NoEntrada = True

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
        entradastr = str(list(self.entrada))
        print(type(self.entrada))
        for e in possibleSteps:
            actuale = list(e)
            if actuale == self.entrada and self.NoEntrada:
                print("ARRIBA spuanchi")
                print(f'Encontraste entrada {actuale} == {self.entrada}')
                self.nexcord = e
                self.NoEntrada = False
            destinoE = list(e)
            if destinoE == self.destino:
                print(f'Encontraste destino {destinoE} == {self.destino}')
                self.nexcord = e
                self.NoDestino = False

        if self.NoDestino and self.NoEntrada:
            for i in possibleSteps:
                cellmates = self.model.grid.get_cell_list_contents(i)
                for j in cellmates:
                    if j.tipo == "semaforo" and j.state is False:
                        # self.parado = True
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
                        self.parado = False
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
                            print(self.prevSentido)
                            if sentido == "<":
                                self.nexcord = ((cord[0] - 1), cord[1])
                                self.prevSentido = sentido
                            elif sentido == ">":
                                self.nexcord = ((cord[0] + 1), cord[1])
                                self.prevSentido = sentido
                            elif sentido == "v":
                                self.nexcord = (cord[0], (cord[1] - 1))
                                self.prevSentido = sentido
                            elif sentido == "^":
                                self.nexcord = (cord[0], (cord[1] + 1))
                                self.prevSentido = sentido
                            elif sentido == "c":
                                if (self.pos == (17, 12) or self.pos == (17, 11))\
                                    and  self.destino[0] < 13\
                                        and self.destino[1] > 11:
                                    self.nexcord = (cord[0], (cord[1] + 1))
                                elif (self.pos == (14, 18) or self.pos == (13, 18))\
                                    and  self.destino[0] < 13\
                                        and self.destino[1] > 11:
                                    self.nexcord = (cord[0], (cord[1] - 1))
                                elif (self.pos == (22, 11) or self.pos == (23, 11))\
                                    and self.destino[0] == 18:
                                    self.nexcord = ((cord[0] - 1), cord[1])
                                elif (self.pos == (22, 11) or self.pos == (23, 11))\
                                    and self.destino[1] > 20:
                                    self.nexcord = (cord[0], (cord[1] + 1))
                                elif (self.pos == (16, 1) or self.pos == (16, 0))\
                                    and self.destino[0] > 18:
                                    self.nexcord = ((cord[0] + 1), cord[1])
                                elif (self.pos == (13, 8) or self.pos == (13, 9))\
                                    and self.destino[1] < 11:
                                    self.nexcord = (cord[0], (cord[1] - 1))
                                elif (self.pos == (7, 11) or self.pos == (7, 12))\
                                    and self.destino[1] > 11:
                                    self.nexcord = (cord[0], (cord[1] + 1))
                                elif (self.pos == (14, 24) or self.pos == (14, 23))\
                                    and self.destino == [5, 15]:
                                    self.nexcord = (cord[0], (cord[1] - 1))
                                elif (self.pos == (14, 24) or self.pos == (14, 23))\
                                    and self.destino == [3, 19]:
                                    self.nexcord = (cord[0], (cord[1] - 1))
                                elif (self.pos == (14, 18) or self.pos == (13, 18))\
                                    and self.destino == [5, 15]:
                                    self.nexcord = (cord[0], (cord[1] - 1))
                                else:
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
                                                        euclidiana(self.entrada, k)
                                                    if distanciaActual > disObjetivo:
                                                        sentido2 = self.model.\
                                                            dicSentido[str(list
                                                                    (n.pos))]
                                                        val = self.\
                                                            validarmov(sentido2,
                                                                    list(n.pos),
                                                                    cord)
                                                        if val:
                                                            distanciaActual =\
                                                                disObjetivo
                                                            Ncord = list(n.pos)
                                                            self.nexcord = (Ncord[0], Ncord[1])
            self.prevcord = self.pos

    def cualesmejor(self,
                       n, Ncord):
        ...

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
        contador = 0
        self.mepuedomover = True

        agente = [agent for agent in self.model.schedule.agents
                  if agent.tipo == "car" and
                  agent.unique_id != self.unique_id and
                  agent.nexcord == self.nexcord]
        agentespos = [agent for agent in self.model.schedule.agents
                      if agent.tipo == "car" and
                      agent.unique_id != self.unique_id and
                      agent.pos == self.nexcord]
        if len(agente) != 0:
            contador = contador + 1
        if contador == 0:
            self.model.grid.move_agent(self, self.nexcord)
        else:
            ...
            if self.parado:
                self.mepuedomover = False
                ...
            else:
                if self.unique_id > agente[0].unique_id:
                    self.parado = False
                    self.model.grid.move_agent(self, self.nexcord)
                else:
                    self.parado = True


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
        self.listaSemaforoContador = None
        self.dicCalles = None
        self.dicHermano = None
        self.dicContrario = None
        self.cuenta = 0


    def modificarcolor(self):
        self.compañero = []
        self.vecinos = []

    def avisarHermano(self, agenteHermano):
        if self.state == True:
            agenteHermano.state = True
        elif self.state == False:
            agenteHermano.state = False

    def contarCoches(self):
        contadorCarros = 0
        posicion = str(list(self.pos))
        vecinos = self.dicCalles[posicion]
        for i in vecinos:
            agentes = self.model.grid.get_cell_list_contents(i)
            for k in agentes:
                if k.tipo == "car":
                    contadorCarros += 1
        return contadorCarros

    def compararContrario(self, agenteContrario, hermanoContrario):
        if self.cuenta < agenteContrario.cuenta:
            self.state = False
            agenteContrario.state = True
            hermanoContrario.state = True
        elif self.cuenta > agenteContrario.cuenta:
            self.state = True
            agenteContrario.state = False
            hermanoContrario.state = False
        # Ya que esta funcion solo la correran los prioritaros
        # si los cont son iguales, el prioritario sera el verde
        else:
            self.state = True
            agenteContrario.state = False
            hermanoContrario.state = False


    def step(self):
        if self.pos in self.listaSemaforoContador:
            self.cuenta = self.contarCoches()
            posicion = str(list(self.pos))
            hermano = self.dicHermano[posicion]
            agenteHermano = self.model.grid.get_cell_list_contents(hermano)

            if posicion in self.dicContrario:
                contrario = self.dicContrario[posicion]
                agenteContrario = self.model.grid.get_cell_list_contents(contrario)
                hermanoContrario = self.dicHermano[str(list(agenteContrario[0].pos))]
                agenteHermanoContrario = self.model.grid.get_cell_list_contents(hermanoContrario)
                self.compararContrario(agenteContrario[0], agenteHermanoContrario[0])
                self.avisarHermano(agenteHermano[0])


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
        self.parada = False

    def step(self):
        pass

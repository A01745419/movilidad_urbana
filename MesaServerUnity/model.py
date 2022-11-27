from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from agent import *
import json


class RandomModel(Model):
    """
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):

        dataDictionary = json.load(open("mapDictionary.json"))
        initCar = []
        numcar = 0
        self.destino = []
        self.traffic_lights = []
        self.dicSentido = {}
        self.dicEntrada = {'[3, 22]': [3, 23],
                           '[21, 22]': [21, 23],
                           '[12, 20]': [13, 20],
                           '[18, 20]': [17, 20],
                           '[3, 19]': [3, 18],
                           '[2, 15]': [1, 15],
                           '[5, 15]': [6, 15],
                           '[12, 15]': [13, 15],
                           '[18, 14]': [17, 14],
                           '[10, 7]': [10, 8],
                           '[21, 5]': [22, 5],
                           '[5, 4]': [6, 4],
                           '[12, 4]': [13, 4],
                           '[19, 2]': [19, 1]}

        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus=False)
            self.schedule = SimultaneousActivation(self)

            # Este for lee el archivo txt para dibujar el mapa
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    # Si el vaor es una calle es porque tiene estas flechas
                    if col in ["v", "^", ">", "<", "c"]:
                        # DataDictionary tiene el sentido de la calla
                        agent = Road(f"r_{r*self.width+c}", self,
                                     dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        initCar.append([c, self.height - r - 1])
                        key = str([c, self.height - r - 1])
                        self.dicSentido[key] = col

                    # Genera los agentes SEMAFORO
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}",
                                              self,
                                              False if col == "S"
                                              else True,
                                              int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    # Genera los edificios
                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    # Genera los puentos de destino
                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destino.append([c, self.height - r - 1])
        # Generar Carros
        for i in range(5):
            numcar += 1
            ran = self.random.choice(initCar)
            car = Car(numcar, self)
            self.grid.place_agent(car, (ran[0], ran[1]))
            self.schedule.add(car)
            car.destino = self.random.choice(self.destino)
            car.entrada = self.dicEntrada[str(car.destino)]
            print(f'Destinos {car.destino} del carro ubicado en {car.pos}')
            print(f'Entrada {car.entrada} del carro ubicado en {car.pos}')

        # for i in self.dicSentido:w
        #     print(i)
        #     print(self.dicSentido[i])
        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()

"""
Modelo de Transito de Coches en Ciudad con Semaforos Inteligentes
Autores: Jose Luis Madrigal, Cesar Emiliano Palome, Christian Parrish y Jorge Blanco
Creado: Noviembre 21, 2022
"""
from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from agent import *
import json
from mesa.datacollection import DataCollector


class RandomModel(Model):
    """
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):

        dataDictionary = json.load(open("mapDictionary.json"))
        # Posibles posiciones donde pueden iniciar los coches
        self.initCar = []
        # Posibles destinos de los coches
        self.destino = []
        self.traffic_lights = []
        self.dicSentido = {}
        self.numAgents = N
        self.running = True
        self.totalMovements = 0
        self.dataCollectorCars = DataCollector(
            model_reporters={"Total Cars Not In Destination":RandomModel.getCarsNotDestination},
            agent_reporters={}
        )
        self.dataCollectorMovements = DataCollector(
            model_reporters={"Total Movements Cars":RandomModel.calculateMovements},
            agent_reporters={}
        )
        self.carsInDestination = []
        
        # Se guardan las celdas de las calles que estan junto a cada destino para que
        # los coches puedan entrar cuando lo encuentren.
        self.dicEntrada = {'[3, 22]': [3, 23],
                           '[21, 22]': [22, 22],
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

        # Ya que un semaforo completo es representado por 2 agentes en diferentes celdas, se elige 1 
        # de cada pareja para hacer el conteo 1 sola vez.
        self.listaSemaforoContador = [(0, 13), (2, 11), (5, 0), (7, 2), (7, 16), (8, 18),
                                      (12, 0), (14, 2), (16, 22), (18, 24), (21, 9), (23, 7)]

        # Una celda semaforo desiganda como contadora puede sensar hasta 8 celdas, debido a que revisa
        # las 3 celdas de ambos carriles de su calle (6) y tambien su propia celda y la de su hermano (2).
        self.dicSemaforoCalles = {'[0, 13]': [(0, 13),(0, 14),(0, 15),(0, 16),(1, 13),(1, 14),(1, 15),(1, 16)],
                                 '[2, 11]': [(2, 11),(3, 11),(4, 11),(5, 11),(2, 12),(3, 12),(4, 12),(5, 12)],
                                 '[5, 0]': [(2, 0),(3, 0),(4, 0),(5, 0),(2, 1),(3, 1),(4, 1),(5, 1)],
                                 '[7, 2]': [(6, 2),(6, 3),(6, 4),(6, 5),(7, 2),(7, 3),(7, 4),(7, 5)],
                                 '[7, 16]': [(6, 13),(6, 14),(6, 15),(6, 16),(7, 13),(7, 14),(7, 15),(7, 16)],
                                 '[8, 18]': [(8, 17),(9, 17),(10, 17),(11, 17),(8, 18),(9, 18),(10, 18),(11, 18)],
                                 '[12, 0]': [(9, 0),(10, 0),(11, 0),(12, 0),(9, 1),(10, 1),(11, 1),(12, 1)],
                                 '[14, 2]': [(13, 2),(13, 3),(13, 4),(13, 5),(14, 2),(14, 3),(14, 4),(14, 5)],
                                 '[16, 22]': [(16, 19),(16, 20),(16, 21),(16, 22),(17, 19),(17, 20),(17, 21),(17, 22)],
                                 '[18, 24]': [(18, 23),(19, 23),(20, 23),(21, 23),(18, 24),(19, 24),(20, 24),(21, 24)],
                                 '[21, 9]': [(18, 8),(19, 8),(20, 8),(21, 8),(18, 9),(19, 9),(20, 9),(21, 9)],
                                 '[23, 7]': [(22, 4),(22, 5),(22, 6),(22, 7),(23, 4),(23, 5),(23, 6),(23, 7)]}

        # Se guardan las celdas de al frente de semaforos prioritarios para evitar choques despues de
        # comparar celdas de calles con contrario (mantiene prioridad hasta que no haya nadie en interseccion)
        self.dicSemaforoPrioritario = {'[0, 13]': [(0, 12),(1, 12)],
                                       '[5, 0]': [(6, 0),(6, 1)],
                                       '[8, 18]': [(7, 17),(7, 18)],
                                       '[12, 0]': [(13, 0),(13, 1)],
                                       '[18, 24]': [(17, 23),(17, 24)],
                                       '[23, 7]': [(22, 8),(23, 8)]}

        # Se relaciona cada semaforo contador con el agente semaforo que esta a su lado para
        # mantener mismo comportamiento en ambos.
        self.dicSemaforoHermano = {'[0, 13]': (1, 13),
                                   '[2, 11]': (2, 12),
                                   '[5, 0]': (5, 1),
                                   '[7, 2]': (6, 2),
                                   '[7, 16]': (6, 16),
                                   '[8, 18]': (8, 17),
                                   '[12, 0]': (12, 1),
                                   '[14, 2]': (13, 2),
                                   '[16, 22]': (17, 22),
                                   '[18, 24]': (18, 23),
                                   '[21, 9]': (21, 8),
                                   '[23, 7]': (22, 7)}

        # Se determinan las celdas semaforo que haran la comparacion con su contrario,
        # para no verificar los contadores mas de una vez. 
        # Esos semaforos seran los que tengan mas prioridad, para que sean los que
        # se pongan verdes si la cuenta es la misma con su contrario. 
        # (Son los que no implican un cambio de sentido o vuelta).
        self.dicSemaforoContrario = {'[0, 13]': (2, 11),
                                     '[5, 0]': (7, 2),
                                     '[8, 18]': (7, 16),
                                     '[12, 0]': (14, 2),
                                     '[18, 24]': (16, 22),
                                     '[23, 7]': (21, 9)}

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
                        self.initCar.append([c, self.height - r - 1])
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
                        agent.listaSemaforoContador = self.listaSemaforoContador
                        agent.dicCalles = self.dicSemaforoCalles
                        agent.dicPrioritario = self.dicSemaforoPrioritario
                        agent.dicHermano = self.dicSemaforoHermano
                        agent.dicContrario = self.dicSemaforoContrario
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
        for i in range(N):
            posInicial = self.random.choice(self.initCar)
            self.initCar.remove(posInicial)
            car = Car(i, self)
            self.grid.place_agent(car, (posInicial[0], posInicial[1]))
            self.schedule.add(car)
            car.destino = self.random.choice(self.destino)
            car.entrada = self.dicEntrada[str(car.destino)]
            print(f'Destino {car.destino} del carro iniciado en {car.pos}')
            print(f'Entrada {car.entrada} del carro iniciado en {car.pos}')
            print(" ")


    def getCarsNotDestination(model):
        '''
        Regresa los coches que no han llegado a su destino en cada step.
        '''
        carsReport = [agent.carsNotDestination for agent in model.schedule.agents if agent.tipo == "car"]
        if len(carsReport) == 0:
            return 0
        else:
            for x in carsReport:
                return x

    def calculateMovements(self):
        '''
        Regresa los movimientos totales que van realizando todos los agentes
        carro en cada step.
        '''
        movementsReport = [agent.movimientos for agent in self.schedule.agents if agent.tipo == "car"]
        for x in movementsReport:
            self.totalMovements += x
        return self.totalMovements


    def step(self):
        '''Avanza el modelo por un paso.'''
        self.schedule.step()
        self.dataCollectorCars.collect(self)
        self.dataCollectorMovements.collect(self)
        print(f'El numero de coches restantes que no han llegado a su destino es: {self.numAgents}')
        if len(self.carsInDestination) > 0:
            for x in self.carsInDestination:
                if x.pos != None:
                    print(f'Modelo elimina a {x.pos} porque llego a su destino')
                    self.grid.remove_agent(x)
                    self.schedule.remove(x)
                    self.carsInDestination.remove(x)

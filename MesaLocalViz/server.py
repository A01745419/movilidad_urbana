"""
Servidor Local con Vizualizador de Mesa de Transito de Coches en Ciudad con Semaforos Inteligentes
Autores: Jose Luis Madrigal, Cesar Emiliano Palome, Christian Parrish y Jorge Blanco
Creado: Noviembre 21, 2022
"""
from agent import *
from model import RandomModel
from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule


def agent_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "w": 1,
                 "h": 1
                 }

    if (isinstance(agent, Road)):
        # Calle
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0

    if (isinstance(agent, Destination)):
        # Se Estacionamiento en verde
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0

    if (isinstance(agent, Traffic_Light)):
        # Se maforo en rojo o verde
        portrayal["Color"] = "red" if not agent.state else "green"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if (isinstance(agent, Obstacle)):
        # Edificios
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if (isinstance(agent, Car)):
        # Edificios
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    return portrayal


width = 0
height = 0

with open('2022_base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0]) - 1
    height = len(lines)

model_params = {"N": 30}

carsLeftGraph = ChartModule([{"Label": "Total Cars Not In Destination", "Color": "Blue"}], data_collector_name='dataCollectorCars')

movementsGraph = ChartModule([{"Label": "Total Movements Cars", "Color": "Red"}], data_collector_name='dataCollectorMovements')

grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

server = ModularServer(RandomModel, [grid, movementsGraph, carsLeftGraph], "Traffic Base", model_params)

server.port = 8521  # The default
server.launch()

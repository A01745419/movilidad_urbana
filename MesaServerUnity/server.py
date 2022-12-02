# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

# Size of the board:
# ancho = 15
# alto = 15
# robots = 5
# cajas = 20
# pasos = 5000000
# grid = CanvasGrid(ancho, alto, 750, 750)

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))

        print(request.form)
        print(number_agents)
        randomModel = RandomModel(number_agents)
        currentStep = 0

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = [{"id": str(agent.unique_id), "x": x, "y":1, "z":z, "desaparece": bool(agent.desaparece)} for (a, x, z) in randomModel.grid.coord_iter() for agent in a if isinstance(agent, Car)]

        return jsonify({'positions':agentPositions})
@app.route('/getSemaforos', methods=['GET'])
def getTrafficLight():
    global randomModel

    if request.method == 'GET':
        semaforosPositions = [{"id": str(agent.unique_id), "x": x, "y":1, "z":z, "state": bool(agent.state), "orientacion": agent.orientacion} for (a, x, z) in randomModel.grid.coord_iter() for agent in a if isinstance(agent, Traffic_Light)]

        return jsonify({'positions':semaforosPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Number of agents {number_agents}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)

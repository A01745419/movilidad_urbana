from flask import Flask, request, jsonify
from mesa.visualization.modules import CanvasGrid
from model import *
from mesa.visualization.ModularVisualization import ModularServer

app = Flask("Traffic example")

with open('2022_base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents, width, height

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        #width = int(request.form.get('width'))
        #height = int(request.form.get('height'))
        pasos = int(request.form.get('pasos'))  
        currentStep = 0

        print(request.form)
        print(number_agents, width, height)
        randomModel = RandomModel(width, height, number_agents, pasos)

        return jsonify({"message":"Parameters recieved, model initiated."})

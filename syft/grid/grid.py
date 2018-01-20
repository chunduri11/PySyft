import syft.controller
import syft.nn as nn
import json

class Grid():

    def __init__(self):
        self.controller = syft.controller

    def configuration(self, model, lr):
        configuration = GridConfiguration(model, lr)
        return configuration

    def learn(self, input, target, configurations):
        configurations_json = list(map(lambda x: x.toJSON(), configurations))
        self.jobId = self.controller.send_json({"objectType": "Grid",
                                   "functionCall": "learn",
                                   "tensorIndexParams": [input.id, target.id],
                                   "configurations": configurations_json})

    def getResults(self):
        results = self.controller.send_json({
            "objectType": "Grid",
            "functionCall": "getResults",
            "experimentId": self.jobId
        })

        modelIds = json.loads(results)
        return ExperimentResults(list(map(lambda id: nn.Sequential(id=id), modelIds)))

class ExperimentResults():
    def __init__(self, models):
        self.results = models

class GridConfiguration():
    def __init__(self, model, lr):
        self.model = model
        self.lr = lr

    def toJSON(self):
        return {"model": self.model.id,
                "lr": self.lr}

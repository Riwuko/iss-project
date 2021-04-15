import json

import flask
from flask import jsonify, request
from flask_cors import CORS

from control_system.utils import get_models_dict, get_models_list
from control_system.process_simulator import ProcessSimulator
from control_system import controllers, processes
from control_system.controllers.controller_model import ControllerModel
from control_system.processes.process_model import ProcessModel

app = flask.Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def process_list():
    return jsonify(get_models_list(processes))

@app.route("/controllers", methods=["GET"])
def controllers_list():
    return jsonify(get_models_list(controllers))

@app.route("/controllers/config", methods=["GET"])
def controllers_config():
    simulation_time = request.args.get("time")
    return jsonify(ControllerModel.get_default_controller_config(simulation_time))

@app.route("/process", methods=["GET"])
def process_config():
    return jsonify(ProcessModel.get_default_simulation_config())


@app.route("/process/<process_slug>", methods=["GET", "POST"])
def simulate_process(process_slug):
    process = get_models_dict(processes).get(process_slug)
    if not process:
        flask.abort(404)

    ps = ProcessSimulator(process_dict=process)
    ps.simulation_config = request.json.get("config", {}) if request.json else {}
    
    if request.args.get("controller"):
        controller = get_models_dict(controllers).get(request.args.get("controller"))
        ps.controller_dict = controller
        ps.controller_config = request.json.get("controller_config", {}) if request.json else {}

    return jsonify(ps.simulate())


def main():
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()

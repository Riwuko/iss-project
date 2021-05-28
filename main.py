import json

import flask
from flask import jsonify, request
from flask_cors import CORS

from control_system.utils import get_models_dict, get_models_list, get_project_items
from control_system.process_simulator import ProcessSimulator
from control_system import controllers, processes, tuners
from control_system.controllers.base_controller_model import ControllerModel
from control_system.processes.base_process_model import ProcessModel
from control_system.tuners.base_tuner_model import TunerModel

app = flask.Flask(__name__)
CORS(app)

project_items = get_project_items()

@app.route("/", methods=["GET"])
def process_list():
    return jsonify(project_items.get("process_list", []))

@app.route("/controllers", methods=["GET"])
def controllers_list():
    return jsonify(project_items.get("controller_list", []))

@app.route("/tuners", methods=["GET"])
def tuners_list():
    return jsonify(project_items.get("tuner_list", []))

@app.route("/controller", methods=["GET"])
def controllers_config():
    simulation_time = request.args.get("simulation_time")
    time_steps = request.args.get("time")
    return jsonify(ControllerModel.get_default_config(time_steps, simulation_time))

@app.route("/process", methods=["GET"])
def process_config():
    return jsonify(ProcessModel.get_default_config())

@app.route("/tuner", methods=["GET"])
def tuner_config():
    return jsonify(TunerModel.get_default_config())

@app.route("/process/<process_slug>", methods=["GET", "POST"])
def simulate_process(process_slug):
    process = project_items.get("process_dict", {}).get(process_slug)
    if not process:
        flask.abort(404)

    ps = ProcessSimulator(process_dict=process)
    ps.simulation_config = request.json.get("config", {}) if request.json else {}
    
    if request.args.get("controller"):
        controller = project_items.get("controller_dict", {}).get(request.args.get("controller"))
        controller_config = request.json.get("controller_config", {}) if request.json else {}
        controller_tuning = project_items.get("tuner_dict", {}).get(request.args.get("tuner"))
        controller_tuning_config = request.json.get("tuner_config", {}) if request.json else {}
        ps.controller_dict = controller
        ps.controller_config = controller_config
        ps.controller_tuning_dict = controller_tuning
        ps.controller_tuning_config = controller_tuning_config

    return jsonify(ps.simulate())


def main():
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()

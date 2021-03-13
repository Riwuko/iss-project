import json

import flask
from flask import jsonify, request
from flask_cors import CORS

from control_system.process_simulator import ProcessSimulator

app = flask.Flask(__name__)
CORS(app)

@app.route("/")
def process_list():
    return jsonify(ProcessSimulator.get_process_list())

@app.route("/process", methods=["GET"])
def process_config():
    ps = ProcessSimulator()
    return jsonify(ps.get_default_simulation_config())


@app.route("/process/<process_slug>", methods=["GET", "POST"])
def simulate_process(process_slug):
    process = ProcessSimulator.get_process_dict().get(process_slug)
    if not process:
        flask.abort(404)

    default_config = ProcessSimulator.get_default_simulation_config()
    config = request.json.get("config", default_config) if request.json else default_config

    tank_area=config.get("tank_area", 1)
    min_level=config.get("min_level", 0)
    max_level=config.get("max_level", 20000)

    process = process.get("process_class")(tank_area)
    ps = ProcessSimulator(process)
    return jsonify(ps.simulate(config))


def main():
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()

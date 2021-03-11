import flask
from flask import request, jsonify
import json
from control_system.process_simulator import ProcessSimulator

app = flask.Flask(__name__)


@app.route('/')
def process_list():
    return jsonify(ProcessSimulator.get_process_list())


@app.route("/process/<process_slug>",  methods=['GET', 'POST'])
def simulate_process(process_slug):
    process = ProcessSimulator.get_process_dict().get(process_slug)
    if not process:
        flask.abort(404)
    process = process.get("process_class")()
    ps = ProcessSimulator(process)

    if request.method == 'GET':
        config = ps.get_default_simulation_config()
    else:
        config = request.json.get("config", {})
        
    response = {
        "config": ps.config,
        "results": ps.simulate(config),
    }
    return jsonify(response)


def main():
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )


if __name__ == "__main__":
    main()

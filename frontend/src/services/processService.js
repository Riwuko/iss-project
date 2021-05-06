const ADDRESS = "http://localhost:8080/";

export function getList() {
  return fetch(ADDRESS).then((data) => data.json());
}

export function getControllerList() {
  return fetch(ADDRESS + "controllers").then((data) => data.json());
}

export function getTunerList() {
  return fetch(ADDRESS + "tuners").then((data) => data.json());
}

export function getConfig() {
  return fetch(ADDRESS + "process").then((data) => data.json());
}

export function getControllerConfig(simulation_time) {
  return fetch(
    ADDRESS +
      "controller?" +
      new URLSearchParams({
        time: simulation_time,
      })
  ).then((data) => data.json());
}

export function getProcess(
  process,
  config,
  controller = "",
  controllerConfig = {},
  tuner = ""
) {
  return fetch(
    ADDRESS +
      "process/" +
      process +
      "?" +
      new URLSearchParams({
        controller: controller,
        tuner,
      }),
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        config: config,
        controller_config: controllerConfig,
      }),
    }
  ).then((data) => data.json());
}

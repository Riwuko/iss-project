const ADDRESS = "http://localhost:8080/";

export async function getList() {
  const data = await fetch(ADDRESS);
  return await data.json();
}

export async function getControllerList() {
  const url = new URL(`${ADDRESS}controllers`);
  const data = await fetch(url);
  return await data.json();
}

export async function getTunerList() {
  const url = new URL(`${ADDRESS}tuners`);
  const data = await fetch(url);
  return await data.json();
}

export async function getConfig() {
  const url = new URL(`${ADDRESS}process`);
  const data = await fetch(url);
  return await data.json();
}

export async function getTunerConfig() {
  const url = new URL(`${ADDRESS}tuner`);
  const data = await fetch(url);
  return await data.json();
}

export async function getControllerConfig(timeSteps, simulationTime) {
  const url = new URL(`${ADDRESS}controller`);
  url.search = new URLSearchParams({
    time: timeSteps,
    simulation_time: simulationTime,
  });
  const data = await fetch(url);
  return await data.json();
}


export async function getProcess(
  process,
  config,
  controller = "",
  controllerConfig = {},
  tuner = "",
  tunerConfig = {},
) {
    const url = new URL(`${ADDRESS}process/${process}`);
    url.search = new URLSearchParams({
      controller: controller,
      tuner: tuner,
    });
    const data = await fetch(
      url,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          config: config,
          controller_config: controllerConfig,
          tuner_config: tunerConfig,
        }),
      }
    );
    return await data.json();
}

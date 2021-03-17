const ADDRESS = "http://localhost:8080/";

export function getList() {
  return fetch(ADDRESS).then((data) => data.json());
}

export function getConfig() {
  return fetch(ADDRESS + "process").then((data) => data.json());
}

export function getProcess(process, config) {
  return fetch(ADDRESS + "process/" + process, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ config: config }),
  }).then((data) => data.json());
}

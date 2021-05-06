import React, { useState, useEffect } from "react";
import { getProcess } from "../services/processService";

import Chart from "./Chart";

const ProcessChart = (props) => {
  const [
    controlValueData,
    simulationResults,
    inputValvesData,
    setPointsData,
  ] = useSelectProcessData(props);

  return (
    <div className="right-charts-container">
      <ControlValueData
        setPointsData={setPointsData}
        controlValueData={controlValueData}
      />
      {simulationResults.map((property, i) => (
        <div key={i}>
          <Chart
            labels={property.times}
            title={property.title}
            datasets={[{ label: property.name, data: property.results }]}
          />
        </div>
      ))}
      <InputsData inputValvesData={inputValvesData} />
    </div>
  );
};

const ControlValueData = ({ setPointsData, controlValueData }) => {
  const controlValueDataSet = [];
  if (setPointsData) {
    controlValueDataSet.push({
      label: "set points",
      fill: false,
      data: setPointsData.values,
    });
  }

  controlValueDataSet.push({
    label: controlValueData?.name,
    data: controlValueData?.results,
  });

  return (
    <div>
      <Chart
        labels={controlValueData?.times}
        title={controlValueData?.name}
        datasets={controlValueDataSet}
      />
    </div>
  );
};

const InputsData = ({ inputValvesData }) => {
  const { title, times: labels } = inputValvesData[0] || {};
  const inputs = inputValvesData.map(({ name, results }) => ({
    label: name,
    fill: false,
    data: results,
  }));

  return (
    <div>
      <Chart labels={labels} title={title} datasets={inputs} />
    </div>
  );
};

const separateData = (items, controlValueName) => {
  const isInput = ([name]) => name.includes("input");
  const isControlValue = ([name]) => name.includes(controlValueName);
  const isSetPoint = ([name]) => name.includes("set_points");

  const [, controlValue] = Object.entries(items).find(isControlValue);
  const inputValves = Object.entries(items)
    .filter(isInput)
    .map(([, item]) => item);
  const results = Object.entries(items)
    .filter(
      (entry) => !(isControlValue(entry) || isInput(entry) || isSetPoint(entry))
    )
    .map(([, item]) => item);
  const setPoints = Object.entries(items)
    .filter((entry) => isSetPoint(entry))
    .map(([, item]) => item);
  return [controlValue, inputValves, results, setPoints];
};

const useSelectProcessData = ({
  controlValue: controlValueName,
  processType,
  simulationConfig,
  controllerType,
  controllerConfig,
  tunerType,
}) => {
  const [controlValueData, setControlValueData] = useState();
  const [simulationResults, setSimulationResults] = useState([]);
  const [inputValvesData, setInputValvesData] = useState([]);
  const [setPointsData, setSetPointsData] = useState();

  useEffect(() => {
    getProcess(
      processType,
      simulationConfig,
      controllerType,
      controllerConfig,
      tunerType
    )
      .then((items) => {
        if (controlValueName) {
          const [
            controlValue,
            inputValvesData,
            simulationResults,
            setPoints,
          ] = separateData(items, controlValueName);
          setControlValueData(controlValue);
          setSimulationResults(simulationResults);
          setInputValvesData(inputValvesData);
          setSetPointsData(...setPoints);
        }
      })
      .catch(console.error);
  }, [
    controlValueName,
    processType,
    simulationConfig,
    controllerType,
    controllerConfig,
    tunerType,
  ]);

  return [controlValueData, simulationResults, inputValvesData, setPointsData];
};

export default ProcessChart;

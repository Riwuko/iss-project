import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { getProcess } from "../../services/processService";

import Chart from "../../shared/Chart";
import { selectProcessType, selectProcessConfig, selectControllerType, selectControllerConfig, selectTunerType, selectControlValueName, selectTunerConfig } from "../selectors";

const ProcessChart = () => {
  const [
    controlValueData,
    simulationResults,
    inputValvesData,
    setPointsData,
  ] = useSelectProcessData();

  return (
    <>
      <ControlValueData
        setPointsData={setPointsData}
        controlValueData={controlValueData}
      />
      <SimulationData simulationData={simulationResults} />
      <InputsData inputValvesData={inputValvesData} />
    </>
  );
};

const SimulationData = ({ simulationData }) => {
  if (simulationData.length>0)
  return (
    simulationData.map((property, i) => (
      <div key={i}>
        <Chart
          labels={property.times}
          title={property.title}
          datasets={[{ label: property.name, data: property.results }]}
        />
      </div>
    ))
  )
  else return null;
};

const ControlValueData = ({ setPointsData, controlValueData }) => {
  const controlValueDataSet = [];
  controlValueDataSet.push({
    label: "set points",
    fill: false,
    data: setPointsData?.values,
  });

  controlValueDataSet.push({
    label: controlValueData?.name,
    data: controlValueData?.results,
  });

  if (controlValueData)
  return (
    <div>
      <Chart
        labels={controlValueData.times}
        title={controlValueData.name}
        datasets={controlValueDataSet}
      />
    </div>
  );
  else return null;
};

const InputsData = ({ inputValvesData }) => {
  const { title, times: labels } = inputValvesData[0] || {};
  const inputs = inputValvesData.map(({ name, results }) => ({
    label: name,
    fill: false,
    data: results,
  }));

 
  if (inputValvesData.length>0)
  return (
    <div>{
      inputValvesData && 
      <Chart labels={labels} title={title} datasets={inputs} />
    }</div>
  );
  else return null;
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

const useSelectProcessData = () => {
  const processType = useSelector(selectProcessType);
  const processConfig = useSelector(selectProcessConfig);
  const controlValueName = useSelector(selectControlValueName);
  const controllerType = useSelector(selectControllerType);
  const controllerConfig = useSelector(selectControllerConfig);
  const tunerType = useSelector(selectTunerType);
  const tunerConfig = useSelector(selectTunerConfig);

  const [controlValueData, setControlValueData] = useState();
  const [simulationResults, setSimulationResults] = useState([]);
  const [inputValvesData, setInputValvesData] = useState([]);
  const [setPointsData, setSetPointsData] = useState();

  useEffect(() => {
    if (processType)
    getProcess(
      processType,
      processConfig,
      controllerType,
      controllerConfig,
      tunerType,
      tunerConfig
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
    processConfig,
    controllerType,
    controllerConfig,
    tunerType,
    tunerConfig,
  ]);

  return [controlValueData, simulationResults, inputValvesData, setPointsData];
};

export default ProcessChart;
